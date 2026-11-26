import json
from datetime import datetime, timedelta, timezone

import pytest

from app.ingest.contract import MESSAGE_FIELDS, SUIZ_AMBIENT, SUIZ_READING, validate_message
from app.ingest.mock_adapter import v1_to_measurement
from app.storage.sqlite import SQLiteMeasurementStore
from simulation.mock_sensors import Fault, Irrigation, generate_messages


START = datetime(2026, 11, 24, 9, tzinfo=timezone(timedelta(hours=3)))
READING = (1, "A", 0, 0, 2000, 2100, 0, 0, 8, 1, 0)
AMBIENT = (1, 0, 0, -1.0, 51.0, 0)


def stream(**settings):
    return list(generate_messages(start=START, seed=42, samples=4, **settings))


def test_v1_fields_follow_the_plan_in_order():
    assert MESSAGE_FIELDS[SUIZ_READING] == (
        "v", "bed", "seq", "up_ms", "soil5_adc", "soil10_adc",
        "soil5_st", "soil10_st", "flow_pulses", "tank_ok", "pump_on",
    )
    assert MESSAGE_FIELDS[SUIZ_AMBIENT] == (
        "v", "seq", "up_ms", "air_temp_c", "air_rh_pct", "dht_st",
    )
    assert validate_message(SUIZ_READING, list(READING)) == READING
    assert validate_message(SUIZ_AMBIENT, list(AMBIENT)) == AMBIENT


def test_irrigate_sends_target_pulses_not_volume():
    # Plan §4.4: calibration stays in Python, so the MCU receives pulses.
    assert MESSAGE_FIELDS["suiz_irrigate"] == (
        "v", "req_id", "bed", "target_pulses", "max_run_s",
    )


@pytest.mark.parametrize(("index", "value", "error"), [
    (0, 2, "v must"),
    (0, True, "v must"),
    (1, "ENV", "bed"),
    (2, -1, "seq"),
    (3, -1, "up_ms"),
    (4, -2, "soil5_adc"),
    (4, -1, "disagree"),
    (5, 2.5, "soil10_adc"),
    (6, 1, "disagree"),
    (7, 2, "soil10_st"),
    (8, -1, "flow_pulses"),
    (9, True, "tank_ok"),
    (10, 2, "pump_on"),
])
def test_reading_rejects_invalid_fields(index, value, error):
    args = list(READING)
    args[index] = value
    with pytest.raises(ValueError, match=error):
        validate_message(SUIZ_READING, args)


@pytest.mark.parametrize(("index", "value", "error"), [
    (2, -1, "up_ms"),
    (3, float("nan"), "air_temp_c"),
    (4, -1, "air_rh_pct"),
    (4, 101, "air_rh_pct"),
    (5, 2, "dht_st"),
])
def test_ambient_rejects_invalid_fields(index, value, error):
    args = list(AMBIENT)
    args[index] = value
    with pytest.raises(ValueError, match=error):
        validate_message(SUIZ_AMBIENT, args)


def test_invalid_message_names_and_argument_counts():
    with pytest.raises(ValueError, match="unsupported measurement message"):
        validate_message("suiz_heartbeat", (1, 0))
    with pytest.raises(ValueError, match="positional sequence"):
        validate_message(SUIZ_READING, dict(zip(MESSAGE_FIELDS[SUIZ_READING], READING)))
    with pytest.raises(ValueError, match="requires 11 arguments"):
        validate_message(SUIZ_READING, READING[:-1])
    with pytest.raises(ValueError, match="requires 6 arguments"):
        validate_message(SUIZ_AMBIENT, (*AMBIENT, 0))


def test_mock_stream_is_deterministic_with_one_ambient_per_sample():
    messages = stream(interval_seconds=30, beds=("B", "A"))
    assert messages == stream(interval_seconds=30, beds=("B", "A"))
    assert all(message["is_synthetic"] is True for message in messages)
    assert len(messages) == 12
    for seq in range(4):
        group = messages[3 * seq:3 * seq + 3]
        assert [message["name"] for message in group] == [
            SUIZ_AMBIENT, SUIZ_READING, SUIZ_READING,
        ]
        ambient, bed_b, bed_a = [
            validate_message(message["name"], message["args"])
            for message in json.loads(json.dumps(group))
        ]
        assert (bed_b.bed, bed_a.bed) == ("B", "A")
        timestamp = START.astimezone(timezone.utc) + timedelta(seconds=30 * seq)
        assert {message["timestamp"] for message in group} == {timestamp.isoformat()}
        for message in (ambient, bed_b, bed_a):
            assert message.seq == seq
            assert message.up_ms == seq * 30_000

    assert stream(beds=("A",)) == [
        message for index, message in enumerate(stream(beds=("B", "A"))) if index % 3 != 1
    ]


def test_v1_keeps_spike_and_freeze_as_raw_behavior():
    baseline = stream(beds=("A",))
    faulty = stream(
        beds=("A",),
        faults=[Fault("A", 5, "spike", 1), Fault("A", 10, "freeze", 1, 2)],
    )
    assert faulty[3]["args"].soil5_adc > baseline[3]["args"].soil5_adc
    assert faulty[3]["args"].soil10_adc == faulty[5]["args"].soil10_adc == baseline[1]["args"].soil10_adc
    assert faulty[3]["args"].soil5_st == faulty[3]["args"].soil10_st == 0
    assert faulty[7] == baseline[7]


def test_irrigation_still_reaches_shallow_probe_first_in_v1():
    baseline = stream(beds=("A",))
    irrigated = stream(beds=("A",), irrigation=[Irrigation("A", sample=1)])
    assert irrigated[3]["args"].soil5_adc < baseline[3]["args"].soil5_adc
    assert irrigated[3]["args"].soil10_adc == baseline[3]["args"].soil10_adc
    assert irrigated[5]["args"].soil10_adc < baseline[5]["args"].soil10_adc


def test_disconnect_sentinel_becomes_none_in_sqlite(tmp_path):
    store = SQLiteMeasurementStore(tmp_path / "v1.sqlite")
    store.initialize()
    messages = stream(faults=[Fault("B", 10, "disconnect", 1)])
    for message in messages:
        assert store.save(v1_to_measurement(message, source="mock")) is True
    for message in messages:
        assert store.save(v1_to_measurement(message, source="mock")) is False

    disconnected = messages[5]["args"]
    assert (disconnected.soil10_adc, disconnected.soil10_st) == (-1, 1)
    records = store.read()
    assert len(records) == 12
    assert all(record.is_synthetic and record.timestamp.tzinfo is timezone.utc for record in records)
    bed_b = store.read(bed_id="B")
    assert bed_b[1].sensors["soil_10cm_adc"] is None
    assert bed_b[1].sensors["soil_5cm_adc"] == disconnected.soil5_adc
    assert bed_b[1].sensors["flow_pulses_total"] == 0
    assert bed_b[1].sensors["up_ms"] == 60_000
    assert bed_b[1].sensors["seq"] == 1
    assert bed_b[2].sensors["soil_10cm_adc"] is not None
    assert len(store.read(bed_id="ENV")) == 4


def test_ambient_error_and_real_provenance_are_preserved(tmp_path):
    store = SQLiteMeasurementStore(tmp_path / "ambient.sqlite")
    store.initialize()
    metadata = {"name": SUIZ_AMBIENT, "timestamp": START.isoformat()}
    mock = v1_to_measurement({**metadata, "args": AMBIENT, "is_synthetic": True}, source="mock")
    real = v1_to_measurement(
        {**metadata, "args": (1, 0, 0, -1.0, -1.0, 1), "is_synthetic": False},
        source="device",
    )
    assert store.save(mock) and store.save(real)
    saved_real, saved_mock = store.read(bed_id="ENV")
    assert saved_real.is_synthetic is False
    assert saved_real.sensors["air_temperature_c"] is None
    assert saved_real.sensors["relative_humidity_pct"] is None
    assert saved_mock.is_synthetic is True
    assert saved_mock.sensors["air_temperature_c"] == -1.0
    assert saved_mock.sensors["relative_humidity_pct"] == 51.0

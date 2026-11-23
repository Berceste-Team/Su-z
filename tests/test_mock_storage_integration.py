from datetime import datetime, timedelta, timezone

import pytest

from app.ingest.mock_adapter import mock_to_measurement
from app.storage.sqlite import SQLiteMeasurementStore
from simulation.mock_sensors import Fault, generate_records


START = datetime(2026, 11, 21, 9, tzinfo=timezone(timedelta(hours=3)))


@pytest.fixture
def store(tmp_path):
    database = SQLiteMeasurementStore(tmp_path / "mock.sqlite")
    database.initialize()
    return database


def test_mock_stream_round_trips_through_sqlite(store):
    records = list(generate_records(
        start=START,
        samples=3,
        seed=42,
        faults=[Fault("B", 10, "disconnect", sample=1)],
    ))
    for record in records:
        assert store.save(mock_to_measurement(record)) is True

    saved = store.read()
    assert len(saved) == 6
    for record, measurement in zip(records, saved):
        assert measurement.bed_id == record["bed_id"]
        assert measurement.timestamp.isoformat() == record["timestamp"]
        assert measurement.timestamp.tzinfo is timezone.utc
        assert measurement.source == "mock-sensors"
        assert measurement.is_synthetic is True
        shallow, deep = record["soil"]
        assert measurement.sensors == {
            "air_temperature_c": record["air_temperature_c"],
            "relative_humidity_pct": record["relative_humidity_pct"],
            "soil_5cm_adc": shallow["raw_adc"],
            "soil_5cm_pct": shallow["moisture_pct"],
            "soil_10cm_adc": deep["raw_adc"],
            "soil_10cm_pct": deep["moisture_pct"],
        }

    bed_b = store.read(bed_id="B")
    assert bed_b[1].sensors["soil_10cm_adc"] is None
    assert bed_b[1].sensors["soil_10cm_pct"] is None
    assert bed_b[2].sensors["soil_10cm_adc"] is not None


def test_offset_timestamp_and_replayed_stream_keep_one_row(store):
    record = next(generate_records(start=START, samples=1, seed=42))
    assert store.save(mock_to_measurement(record)) is True

    replay = next(generate_records(start=START, samples=1, seed=42))
    replay["timestamp"] = START.isoformat()
    assert store.save(mock_to_measurement(replay)) is False
    saved, = store.read()
    assert saved.timestamp.isoformat() == "2026-11-21T06:00:00+00:00"


def test_changed_payload_conflicts_unless_it_has_a_distinct_source(store):
    record = next(generate_records(start=START, samples=1, seed=42))
    first = mock_to_measurement(record, source="mock-run-1")
    assert store.save(first) is True
    record["soil"][0]["raw_adc"] += 1

    with pytest.raises(ValueError, match="identity already exists"):
        store.save(mock_to_measurement(record, source="mock-run-1"))
    assert store.read() == [first]

    second = mock_to_measurement(record, source="mock-run-2")
    assert store.save(second) is True
    assert store.read() == [first, second]


def test_unsampled_channel_stays_absent_after_storage(store):
    record = next(generate_records(start=START, samples=1, seed=42))
    del record["relative_humidity_pct"]
    del record["soil"][0]["moisture_pct"]
    assert store.save(mock_to_measurement(record)) is True
    saved, = store.read()
    assert "relative_humidity_pct" not in saved.sensors
    assert "soil_5cm_pct" not in saved.sensors
    assert saved.sensors["soil_5cm_adc"] == record["soil"][0]["raw_adc"]


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"schema": "other.v1"}, "unsupported mock sensor schema"),
        ({"is_synthetic": False}, "marked synthetic"),
        ({"timestamp": "2026-11-21T06:00:00"}, "timezone-aware"),
        ({"soil": [{"depth_cm": 5}, {"depth_cm": 5}]}, "distinct positive integers"),
    ],
)
def test_adapter_rejects_incompatible_records(changes, message):
    record = next(generate_records(start=START, samples=1, seed=42))
    with pytest.raises(ValueError, match=message):
        mock_to_measurement({**record, **changes})

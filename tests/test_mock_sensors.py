import json
from datetime import datetime, timedelta, timezone

import pytest

from simulation.mock_sensors import Fault, Irrigation, generate_records


START = datetime(2026, 11, 21, 9, tzinfo=timezone(timedelta(hours=3)))


def records(**options):
    return list(generate_records(start=START, seed=42, samples=6, **options))


def test_records_are_reproducible_and_json_compatible():
    first = records()
    assert first == records()
    assert first != list(generate_records(start=START, seed=43, samples=6))
    assert json.loads(json.dumps(first, allow_nan=False)) == first
    assert all(record["is_synthetic"] is True for record in first)
    assert {record["schema"] for record in first} == {"suiz.mock-sensors.provisional.v1"}


def test_both_beds_share_ambient_but_have_distinct_soil_readings():
    first, second = records()[:2]
    assert (first["bed_id"], second["bed_id"]) == ("A", "B")
    assert first["timestamp"] == second["timestamp"] == "2026-11-21T06:00:00+00:00"
    assert first["air_temperature_c"] == second["air_temperature_c"]
    assert first["relative_humidity_pct"] == second["relative_humidity_pct"]
    assert first["soil"] != second["soil"]
    assert records(beds=("B",)) == records()[1::2]


@pytest.mark.parametrize(("options", "seconds"), [({}, 60), ({"interval_seconds": 30}, 30)])
def test_sampling_interval(options, seconds):
    first, second = records(beds=("A",), **options)[:2]
    assert datetime.fromisoformat(second["timestamp"]) - datetime.fromisoformat(
        first["timestamp"]
    ) == timedelta(seconds=seconds)


def test_raw_adc_and_calibrated_moisture_are_separate():
    for probe in records()[0]["soil"]:
        raw = probe["raw_adc"]
        assert type(raw) is int
        assert 0 <= raw <= 4095
        assert probe["moisture_pct"] == round(50 * (3200 - raw) / (3200 - 1300), 2)


def test_irrigation_reaches_shallow_probe_before_deep_probe():
    baseline = records()
    irrigated = records(irrigation=[Irrigation("B", sample=2)])
    before, shallow, deep = irrigated[3], irrigated[5], irrigated[7]
    assert before == baseline[3]
    assert shallow["soil"][0]["moisture_pct"] > before["soil"][0]["moisture_pct"]
    assert shallow["soil"][1] == baseline[5]["soil"][1]
    assert deep["soil"][1]["moisture_pct"] > shallow["soil"][1]["moisture_pct"]
    assert irrigated[::2] == baseline[::2]


@pytest.mark.parametrize("kind", ["spike", "freeze", "disconnect"])
def test_fault_affects_only_target_probe_and_recovers(kind):
    baseline = records(beds=("A",))
    faulty = records(beds=("A",), faults=[Fault("A", 5, kind, 2, 2)])
    assert faulty[:2] == baseline[:2]
    assert faulty[4:] == baseline[4:]
    for index in (2, 3):
        probe = faulty[index]["soil"][0]
        assert probe["status"] == kind
        assert faulty[index]["soil"][1] == baseline[index]["soil"][1]
        if kind == "spike":
            assert probe["raw_adc"] > baseline[index]["soil"][0]["raw_adc"]
            assert probe["moisture_pct"] < baseline[index]["soil"][0]["moisture_pct"]
        elif kind == "freeze":
            assert probe["raw_adc"] == baseline[1]["soil"][0]["raw_adc"]
            assert probe["moisture_pct"] == baseline[1]["soil"][0]["moisture_pct"]
        else:
            assert probe["raw_adc"] is None
            assert probe["moisture_pct"] is None


@pytest.mark.parametrize("options", [
    {"interval_seconds": 0},
    {"beds": ("B", "B")},
    {"irrigation": [Irrigation("B", sample=6)]},
    {"faults": [Fault("A", 5, "freeze", 0, 3), Fault("A", 5, "spike", 2)]},
])
def test_invalid_configuration(options):
    with pytest.raises(ValueError):
        records(**options)


def test_soil_dries_between_irrigation_events():
    dry_run = list(generate_records(start=START, seed=42, samples=120, beds=("A",)))
    for index in (0, 1):
        first = dry_run[0]["soil"][index]
        last = dry_run[-1]["soil"][index]
        assert last["raw_adc"] > first["raw_adc"]
        assert last["moisture_pct"] < first["moisture_pct"]

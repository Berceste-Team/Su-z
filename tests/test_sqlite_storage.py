from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from datetime import datetime, timedelta, timezone

import pytest

from app.storage.measurement import Measurement
from app.storage.sqlite import SQLiteMeasurementStore


START = datetime(2026, 11, 21, 6, tzinfo=timezone.utc)


@pytest.fixture
def store(tmp_path):
    storage = SQLiteMeasurementStore(tmp_path / "measurements.sqlite")
    storage.initialize()
    return storage


@pytest.fixture
def measurement():
    return Measurement(
        bed_id="A",
        timestamp=START,
        source="test-stream",
        is_synthetic=True,
        sensors={"soil_5cm_adc": 2000, "soil_5cm_pct": 31.0, "soil_10cm_adc": None},
    )


def test_round_trip_after_reopening(tmp_path, store, measurement):
    assert store.read() == []
    assert store.save(measurement) is True

    db_path = tmp_path / "measurements.sqlite"
    assert db_path.is_file()
    reopened = SQLiteMeasurementStore(db_path)
    reopened.initialize()
    assert reopened.read() == [measurement]
    assert reopened.read()[0].sensors["soil_10cm_adc"] is None
    assert "soil_10cm_pct" not in reopened.read()[0].sensors


def test_read_orders_by_timestamp_and_can_filter_by_bed(store, measurement):
    later = replace(measurement, timestamp=START + timedelta(microseconds=1))
    other_bed = replace(measurement, bed_id="B")
    for record in (later, other_bed, measurement):
        store.save(record)

    assert store.read() == [measurement, other_bed, later]
    assert store.read(bed_id="B") == [other_bed]
    assert store.read(bed_id="unknown") == []


def test_same_instant_with_different_offset_is_an_identical_retry(store, measurement):
    local_time = START.astimezone(timezone(timedelta(hours=3)))
    retry = replace(
        measurement,
        timestamp=local_time,
        sensors=dict(reversed(tuple(measurement.sensors.items()))),
    )

    assert store.save(measurement) is True
    assert store.save(retry) is False
    assert store.read() == [measurement]
    assert store.read()[0].timestamp.tzinfo == timezone.utc


def test_conflicting_retry_preserves_original(store, measurement):
    store.save(measurement)
    with pytest.raises(ValueError, match="identity already exists"):
        store.save(replace(measurement, sensors={"soil_5cm_adc": 2100}))
    assert store.read() == [measurement]


def test_concurrent_retries_insert_only_one_row(store, measurement):
    with ThreadPoolExecutor(max_workers=2) as executor:
        results = list(executor.map(store.save, [measurement, measurement]))
    assert sorted(results) == [False, True]
    assert store.read() == [measurement]


def test_different_sources_and_synthetic_flags_get_distinct_identities(store, measurement):
    real = replace(measurement, is_synthetic=False)
    other_source = replace(measurement, source="another-stream")

    for record in (measurement, real, other_source):
        assert store.save(record) is True

    assert store.read() == [other_source, real, measurement]


def test_sql_like_metadata_is_stored_and_filtered_as_text(store, measurement):
    sql_like_bed = "A' OR 1=1 --"
    record = replace(measurement, bed_id=sql_like_bed, source="source'); DROP TABLE measurements;")
    store.save(record)
    store.save(measurement)
    assert store.read(bed_id=sql_like_bed) == [record]
    assert len(store.read()) == 2


def test_can_record_an_observation_with_no_sensor_values(store, measurement):
    missing = replace(measurement, sensors={})
    assert store.save(missing) is True
    assert store.read() == [missing]


@pytest.mark.parametrize("value", [float("nan"), float("inf"), float("-inf"), "38", True, {}])
def test_invalid_sensor_values_are_rejected(value, measurement):
    with pytest.raises(ValueError, match="finite number or None"):
        replace(measurement, sensors={"soil_5cm_adc": value})


@pytest.mark.parametrize(
    ("changes", "message"),
    [
        ({"bed_id": ""}, "bed_id"),
        ({"source": " "}, "source"),
        ({"timestamp": START.replace(tzinfo=None)}, "timezone-aware"),
        ({"is_synthetic": 1}, "boolean"),
        ({"sensors": {"": 12}}, "channel names"),
        ({"sensors": None}, "mapping"),
    ],
)
def test_invalid_metadata_is_rejected(changes, message, measurement):
    with pytest.raises(ValueError, match=message):
        replace(measurement, **changes)

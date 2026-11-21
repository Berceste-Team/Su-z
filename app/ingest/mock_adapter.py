"""Translate the provisional mock message into the application measurement model."""

from collections.abc import Mapping
from datetime import datetime

from app.storage.measurement import Measurement


MOCK_SCHEMA = "suiz.mock-sensors.provisional.v1"


def mock_to_measurement(
    record: Mapping, *, source: str = "mock-sensors"
) -> Measurement:
    """Convert a mock v1 record while preserving missing channel values.

    Absent channels stay absent and explicit nulls become None. Probe status
    labels belong to the mock payload and have no field in Measurement.
    Reuse source when retrying a stream. Give independent runs distinct
    source identifiers when their timestamps and beds may overlap.
    """
    if record.get("schema") != MOCK_SCHEMA:
        raise ValueError("unsupported mock sensor schema")
    if record.get("is_synthetic") is not True:
        raise ValueError("mock sensor records must be marked synthetic")

    sensors = {
        field: record[field]
        for field in ("air_temperature_c", "relative_humidity_pct")
        if field in record
    }
    depths = set()
    for probe in record["soil"]:
        depth = probe["depth_cm"]
        if type(depth) is not int or depth <= 0 or depth in depths:
            raise ValueError("mock probe depths must be distinct positive integers")
        depths.add(depth)
        for field, suffix in (("raw_adc", "adc"), ("moisture_pct", "pct")):
            if field in probe:
                sensors[f"soil_{depth}cm_{suffix}"] = probe[field]

    return Measurement(
        bed_id=record["bed_id"],
        timestamp=datetime.fromisoformat(record["timestamp"]),
        source=source,
        is_synthetic=record["is_synthetic"],
        sensors=sensors,
    )

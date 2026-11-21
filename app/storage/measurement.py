"""Provisional application model for measurements, independent of storage."""

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime, timezone
from math import isfinite
from types import MappingProxyType


@dataclass(frozen=True)
class Measurement:
    """One observation from a source stream for one bed.

    Sensor keys identify the channel and unit (for example, soil_5cm_adc).
    Omit channels that were not sampled and use None for a missing or
    unusable value on a sampled channel. A producer can map its wire format
    into this model once the MCU–MPU contract is agreed.
    """

    bed_id: str
    timestamp: datetime
    source: str
    is_synthetic: bool
    sensors: Mapping[str, int | float | None]

    def __post_init__(self) -> None:
        for name, value in (("bed_id", self.bed_id), ("source", self.source)):
            if not isinstance(value, str) or not value.strip():
                raise ValueError(f"{name} must be a nonempty string")
        if not isinstance(self.timestamp, datetime) or self.timestamp.utcoffset() is None:
            raise ValueError("timestamp must be a timezone-aware datetime")
        if type(self.is_synthetic) is not bool:
            raise ValueError("is_synthetic must be a boolean")
        if not isinstance(self.sensors, Mapping):
            raise ValueError("sensors must be a mapping of channels to values")

        sensors = dict(self.sensors)
        for channel, value in sensors.items():
            if not isinstance(channel, str) or not channel.strip():
                raise ValueError("sensor channel names must be nonempty strings")
            if value is None or type(value) is int:
                continue
            if type(value) is not float or not isfinite(value):
                raise ValueError(f"sensor {channel!r} must be a finite number or None")

        object.__setattr__(self, "timestamp", self.timestamp.astimezone(timezone.utc))
        object.__setattr__(self, "sensors", MappingProxyType(sensors))

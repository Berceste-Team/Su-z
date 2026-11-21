"""Local SQLite implementation of measurement storage."""

from contextlib import closing
from datetime import datetime
import json
from pathlib import Path
import sqlite3

from .measurement import Measurement


class SQLiteMeasurementStore:
    """Persist measurements in a local file using short-lived connections.

    The identity is (bed_id, source, timestamp UTC, is_synthetic). Source
    identifies a producer stream. Each stream can emit one measurement per
    bed and timestamp for each synthetic flag.
    """

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path).resolve()

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)

    def initialize(self) -> None:
        """Create the measurement table if it does not already exist."""
        with closing(self._connect()) as connection, connection:
            connection.execute("""
                CREATE TABLE IF NOT EXISTS measurements (
                    bed_id TEXT NOT NULL,
                    source TEXT NOT NULL,
                    timestamp_utc TEXT NOT NULL,
                    is_synthetic INTEGER NOT NULL CHECK (is_synthetic IN (0, 1)),
                    sensors_json TEXT NOT NULL,
                    PRIMARY KEY (bed_id, source, timestamp_utc, is_synthetic)
                )
            """)

    def save(self, measurement: Measurement) -> bool:
        """Insert once and return True, or return False on an identical retry.

        Raise ValueError if the identity already exists with different sensor
        values. The unique key and conflict check share the write transaction.
        """
        identity = (
            measurement.bed_id,
            measurement.source,
            measurement.timestamp.isoformat(timespec="microseconds"),
            measurement.is_synthetic,
        )
        sensors = dict(measurement.sensors)
        encoded = json.dumps(sensors, allow_nan=False)
        with closing(self._connect()) as connection, connection:
            result = connection.execute("""
                INSERT INTO measurements (
                    bed_id, source, timestamp_utc, is_synthetic, sensors_json
                ) VALUES (?, ?, ?, ?, ?)
                ON CONFLICT (bed_id, source, timestamp_utc, is_synthetic) DO NOTHING
            """, (*identity, encoded))
            if result.rowcount == 1:
                return True

            existing, = connection.execute("""
                SELECT sensors_json
                FROM measurements
                WHERE bed_id = ? AND source = ? AND timestamp_utc = ? AND is_synthetic = ?
            """, identity).fetchone()
            if json.loads(existing) != sensors:
                raise ValueError("measurement identity already exists with different sensor values")
            return False

    def read(self, *, bed_id: str | None = None) -> list[Measurement]:
        """Read measurements in UTC timestamp order, optionally for one bed."""
        query = """
            SELECT bed_id, source, timestamp_utc, is_synthetic, sensors_json
            FROM measurements
        """
        parameters = ()
        if bed_id is not None:
            query += " WHERE bed_id = ?"
            parameters = (bed_id,)
        query += " ORDER BY timestamp_utc, bed_id, source, is_synthetic"

        with closing(self._connect()) as connection:
            return [
                Measurement(
                    bed_id=bed,
                    timestamp=datetime.fromisoformat(timestamp),
                    source=source,
                    is_synthetic=bool(is_synthetic),
                    sensors=json.loads(sensors),
                )
                for bed, source, timestamp, is_synthetic, sensors
                in connection.execute(query, parameters)
            ]

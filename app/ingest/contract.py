"""Provisional v1 message definitions from docs/yazilim-plani.md §4.

These definitions cover logical arguments. Transport and hardware details
remain subject to the UNO Q proof of concept and team approval.
"""

from collections.abc import Sequence
from sys import float_info
from typing import NamedTuple


VERSION = 1
UNREADABLE = -1
NORMAL = 0
READ_ERROR = 1

SUIZ_READING = "suiz_reading"
SUIZ_AMBIENT = "suiz_ambient"


class Reading(NamedTuple):
    v: int
    bed: str
    seq: int
    up_ms: int
    soil5_adc: int
    soil10_adc: int
    soil5_st: int
    soil10_st: int
    flow_pulses: int
    tank_ok: int
    pump_on: int


class Ambient(NamedTuple):
    v: int
    seq: int
    up_ms: int
    air_temp_c: float
    air_rh_pct: float
    dht_st: int


MESSAGE_FIELDS = {
    SUIZ_READING: Reading._fields,
    SUIZ_AMBIENT: Ambient._fields,
    "suiz_irrigation_result": ("v", "req_id", "bed", "result", "reason", "run_ms", "pulses"),
    "suiz_safety": ("v", "bed", "code", "up_ms"),
    "suiz_irrigate": ("v", "req_id", "bed", "target_pulses", "max_run_s"),
    "suiz_heartbeat": ("v", "seq"),
    "suiz_reset_lock": ("v", "bed"),
}
EVENT_CODES = frozenset({
    "OK", "TANK_LOW", "BUSY", "MIN_INTERVAL", "DAILY_LIMIT", "LOCKED",
    "BAD_ARGS", "NO_FLOW", "MAX_RUNTIME", "HEARTBEAT_LOST", "BOOT",
})


def _require_counter(field: str, value: int) -> None:
    if type(value) is not int or value < 0:
        raise ValueError(f"{field} must be a nonnegative integer")


def _require_binary(field: str, value: int) -> None:
    if type(value) is not int or value not in (0, 1):
        raise ValueError(f"{field} must be an integer 0 or 1")


def validate_message(name: str, args: Sequence) -> Reading | Ambient:
    """Validate one reading or ambient message and return its named arguments.

    Sequence and uptime are checked per message. Tracking a stream across
    messages (gaps or reboot detection) is the responsibility of its consumer.
    """
    if name not in (SUIZ_READING, SUIZ_AMBIENT):
        raise ValueError(f"unsupported measurement message: {name!r}")
    if not isinstance(args, Sequence) or isinstance(args, (str, bytes, bytearray)):
        raise ValueError("message arguments must be a positional sequence")
    fields = MESSAGE_FIELDS[name]
    if len(args) != len(fields):
        raise ValueError(f"{name} requires {len(fields)} arguments")
    if type(args[0]) is not int or args[0] != VERSION:
        raise ValueError(f"v must be the integer {VERSION}")

    if name == SUIZ_READING:
        reading = Reading(*args)
        if reading.bed not in ("A", "B"):
            raise ValueError("bed must be A or B")
        _require_counter("seq", reading.seq)
        _require_counter("up_ms", reading.up_ms)
        _require_counter("flow_pulses", reading.flow_pulses)
        _require_binary("tank_ok", reading.tank_ok)
        _require_binary("pump_on", reading.pump_on)
        for adc_field, adc, status_field, status in (
            ("soil5_adc", reading.soil5_adc, "soil5_st", reading.soil5_st),
            ("soil10_adc", reading.soil10_adc, "soil10_st", reading.soil10_st),
        ):
            _require_binary(status_field, status)
            if type(adc) is not int or adc < UNREADABLE:
                raise ValueError(f"{adc_field} must be a nonnegative ADC count or -1")
            if (adc == UNREADABLE) != (status == READ_ERROR):
                raise ValueError(f"{adc_field} and {status_field} disagree")
        return reading

    ambient = Ambient(*args)
    _require_counter("seq", ambient.seq)
    _require_counter("up_ms", ambient.up_ms)
    _require_binary("dht_st", ambient.dht_st)
    for field, value in (("air_temp_c", ambient.air_temp_c), ("air_rh_pct", ambient.air_rh_pct)):
        if type(value) not in (int, float) or not -float_info.max <= value <= float_info.max:
            raise ValueError(f"{field} must be a finite number")
    if ambient.dht_st == READ_ERROR and UNREADABLE not in (ambient.air_temp_c, ambient.air_rh_pct):
        raise ValueError("dht_st indicates an error without an unreadable value")
    if not 0 <= ambient.air_rh_pct <= 100 and not (
        ambient.dht_st == READ_ERROR and ambient.air_rh_pct == UNREADABLE
    ):
        raise ValueError("air_rh_pct must be between 0 and 100 or unreadable")
    return ambient

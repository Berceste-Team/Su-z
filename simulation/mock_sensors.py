"""Generate synthetic sensor data without hardware or external dependencies.

Both the legacy record format and the proposed v1 messages are provisional.
Legacy soil readings carry ADC counts and simulated volumetric moisture
percentages. The v1 messages carry raw ADC counts. The 12-bit ADC range and
linear dry/wet calibration are simulation assumptions. The dry and wet
endpoints represent 0% and 50% VWC.
"""

from collections.abc import Iterable, Iterator
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from itertools import groupby
from math import exp, sin, tau
from random import Random
from typing import Literal

from app.ingest.contract import (
    NORMAL,
    READ_ERROR,
    SUIZ_AMBIENT,
    SUIZ_READING,
    UNREADABLE,
    VERSION,
    Ambient,
    Reading,
)

Bed = Literal["A", "B"]
FaultKind = Literal["spike", "freeze", "disconnect"]

DRY_ADC = 3200
WET_ADC = 1300
ADC_MAX = 4095
WET_VWC_PCT = 50.0
DEPTHS_CM = (5, 10)


@dataclass(frozen=True)
class Irrigation:
    """A simulated irrigation event at a zero-based sample index."""

    bed: Bed
    sample: int


@dataclass(frozen=True)
class Fault:
    """Apply a fault to one probe for duration_samples, starting at sample."""

    bed: Bed
    depth_cm: int
    kind: FaultKind
    sample: int
    duration_samples: int = 1


def generate_records(
    *,
    start: datetime,
    samples: int,
    seed: int,
    interval_seconds: int = 60,
    beds: Iterable[Bed] = ("A", "B"),
    irrigation: Iterable[Irrigation] = (),
    faults: Iterable[Fault] = (),
) -> Iterator[dict]:
    """Yield JSON-compatible records in timestamp order, then selected bed order.

    Each time step produces one record per selected bed. Timestamps are emitted
    in UTC. Both beds share ambient readings. With no events the soil dries
    gradually. An irrigation event raises the 5 cm reading immediately and the
    10 cm reading at the next sample. A freeze holds the preceding unperturbed
    raw reading (the initial reading when starting at sample zero).
    """
    if start.tzinfo is None or start.utcoffset() is None:
        raise ValueError("start must include a timezone")
    if samples < 0 or interval_seconds <= 0:
        raise ValueError("samples must be nonnegative and interval_seconds positive")
    start = start.astimezone(timezone.utc)
    beds = tuple(beds)
    if not beds or any(bed not in ("A", "B") for bed in beds) or len(set(beds)) != len(beds):
        raise ValueError("beds must contain distinct selections from A and B")

    irrigation_samples = {bed: set() for bed in beds}
    for event in irrigation:
        if event.bed not in beds or not 0 <= event.sample < samples:
            raise ValueError("irrigation must target a selected bed and sample")
        irrigation_samples[event.bed].add(event.sample)

    faults_by_probe = {(bed, depth): [] for bed in beds for depth in DEPTHS_CM}
    for fault in faults:
        probe = (fault.bed, fault.depth_cm)
        end = fault.sample + fault.duration_samples
        if (probe not in faults_by_probe or fault.kind not in ("spike", "freeze", "disconnect")
                or not 0 <= fault.sample < end <= samples):
            raise ValueError("fault must target a selected probe and valid sample range")
        faults_by_probe[probe].append(fault)
    for schedule in faults_by_probe.values():
        schedule.sort(key=lambda fault: fault.sample)
        for previous, current in zip(schedule, schedule[1:]):
            if previous.sample + previous.duration_samples > current.sample:
                raise ValueError("faults on the same probe must not overlap")

    ambient_rng = Random(f"{seed}:ambient")
    probe_rngs = {probe: Random(f"{seed}:{probe[0]}:{probe[1]}") for probe in faults_by_probe}
    moisture = {
        (bed, depth): (31.0 if bed == "A" else 29.0) + (2.0 if depth == 10 else 0.0)
        for bed, depth in faults_by_probe
    }
    previous_adc = {}
    frozen_adc = {}
    # Exponential drying keeps VWC between the dry baseline and the wet bound.
    retention = exp(-interval_seconds / (48 * 3600))
    for sample in range(samples):
        timestamp = start + timedelta(seconds=sample * interval_seconds)
        day_phase = tau * (timestamp.hour * 3600 + timestamp.minute * 60 + timestamp.second) / 86400
        daily_cycle = sin(day_phase - tau * 8 / 24)
        temperature_c = round(22 + 3 * daily_cycle + ambient_rng.uniform(-0.2, 0.2), 2)
        relative_humidity_pct = round(60 - 8 * daily_cycle + ambient_rng.uniform(-0.5, 0.5), 2)
        for bed in beds:
            soil = []
            for depth in DEPTHS_CM:
                probe = (bed, depth)
                if sample:
                    moisture[probe] = 12 + (moisture[probe] - 12) * retention
                delay = 0 if depth == 5 else 1
                if sample - delay in irrigation_samples[bed]:
                    gain = 7 if depth == 5 else 4
                    moisture[probe] = min(WET_VWC_PCT, moisture[probe] + gain)
                adc = round(DRY_ADC + (WET_ADC - DRY_ADC) * moisture[probe] / WET_VWC_PCT)
                adc += probe_rngs[probe].randint(-3, 3)
                raw_adc = adc
                status = "normal"
                schedule = faults_by_probe[probe]
                if schedule and schedule[0].sample <= sample:
                    fault = schedule[0]
                    status = fault.kind
                    if status == "spike":
                        raw_adc = min(ADC_MAX, adc + 850)
                    elif status == "freeze":
                        if sample == fault.sample:
                            frozen_adc[probe] = previous_adc.get(probe, adc)
                        raw_adc = frozen_adc[probe]
                    else:
                        raw_adc = None
                    if sample + 1 == fault.sample + fault.duration_samples:
                        schedule.pop(0)
                previous_adc[probe] = adc
                moisture_pct = None
                if raw_adc is not None:
                    fraction = (DRY_ADC - raw_adc) / (DRY_ADC - WET_ADC)
                    moisture_pct = round(WET_VWC_PCT * min(1, max(0, fraction)), 2)
                soil.append({
                    "depth_cm": depth,
                    "raw_adc": raw_adc,
                    "moisture_pct": moisture_pct,
                    "status": status,
                })
            yield {
                "schema": "suiz.mock-sensors.provisional.v1",
                "timestamp": timestamp.isoformat(),
                "bed_id": bed,
                "is_synthetic": True,
                "air_temperature_c": temperature_c,
                "relative_humidity_pct": relative_humidity_pct,
                "soil": soil,
            }


def generate_messages(
    *,
    start: datetime,
    samples: int,
    seed: int,
    interval_seconds: int = 60,
    beds: Iterable[Bed] = ("A", "B"),
    irrigation: Iterable[Irrigation] = (),
    faults: Iterable[Fault] = (),
) -> Iterator[dict]:
    """Yield v1 argument lists with Python-side timestamps and provenance.

    Each sample yields ambient once, then one reading per selected bed. Each
    bed and the ambient stream count samples from zero on a shared uptime.
    Flow, tank and pump fields are idle placeholders. Irrigation changes the
    simulated soil only.
    """
    if type(interval_seconds) is not int:
        raise ValueError("interval_seconds must be an integer for v1 messages")
    records = generate_records(
        start=start,
        samples=samples,
        seed=seed,
        interval_seconds=interval_seconds,
        beds=beds,
        irrigation=irrigation,
        faults=faults,
    )
    for seq, (timestamp, sample) in enumerate(groupby(records, key=lambda record: record["timestamp"])):
        up_ms = seq * interval_seconds * 1000
        metadata = {"timestamp": timestamp, "is_synthetic": True}
        for index, record in enumerate(sample):
            if index == 0:
                yield {
                    **metadata,
                    "name": SUIZ_AMBIENT,
                    "args": Ambient(
                        v=VERSION,
                        seq=seq,
                        up_ms=up_ms,
                        air_temp_c=record["air_temperature_c"],
                        air_rh_pct=record["relative_humidity_pct"],
                        dht_st=NORMAL,
                    ),
                }

            shallow, deep = record["soil"]
            adc5, adc10 = shallow["raw_adc"], deep["raw_adc"]
            yield {
                **metadata,
                "name": SUIZ_READING,
                "args": Reading(
                    v=VERSION,
                    bed=record["bed_id"],
                    seq=seq,
                    up_ms=up_ms,
                    soil5_adc=UNREADABLE if adc5 is None else adc5,
                    soil10_adc=UNREADABLE if adc10 is None else adc10,
                    soil5_st=READ_ERROR if adc5 is None else NORMAL,
                    soil10_st=READ_ERROR if adc10 is None else NORMAL,
                    flow_pulses=0,
                    tank_ok=1,
                    pump_on=0,
                ),
            }

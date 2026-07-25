"""Canonical dementia-signal vocabulary shared across the platform.

These string values ARE the wire/storage/metrics vocabulary. They must equal the
``DementiaSignalKind`` / ``DementiaSignalSeverity`` proto enum names (lowercased,
prefix-stripped) in ``continuoustracking/v1/signals.proto``. The publisher, CC
subscriber, and CC signal_config consume this enum.

Two-sided rule:
* Wire kinds live here in ``cts_contracts.DementiaSignalKind``.
* CC-local kinds live in ``signal_config.CC_LOCAL_SIGNAL_KINDS``.

``StrEnum`` members compare equal to their string value, so existing code that compares against
``"stillness_anomaly"`` keeps working during migration.
"""

from __future__ import annotations

from enum import StrEnum


class DementiaSignalKind(StrEnum):
    """A dementia-care behavioural signal kind.

    Members and order mirror the wire enum
    ``continuoustracking.v1.DementiaSignalKind`` (values 1..10; ``UNSPECIFIED`` = 0 is
    intentionally omitted: it is never a valid emitted kind).
    """

    PACING = "pacing"
    SUNDOWNING_INDEX = "sundowning_index"
    BATHROOM_DWELL_ANOMALY = "bathroom_dwell_anomaly"
    NIGHTTIME_MOVEMENT = "nighttime_movement"
    STILLNESS_ANOMALY = "stillness_anomaly"
    ABSENCE = "absence"
    FALL_SUSPECTED = "fall_suspected"
    GAIT_SLOWING = "gait_slowing"
    AGITATION_INDEX = "agitation_index"
    SAME_CLOTHES_SUSPECTED = "same_clothes_suspected"

    @classmethod
    def from_wire(cls, value: str) -> DementiaSignalKind | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown.

        Unknown kinds must render generically rather than crash (the platform's
        forward-compatibility rule), so callers handle ``None`` explicitly instead of
        this raising.
        """
        try:
            return cls(value)
        except ValueError:
            return None


class DementiaSignalSeverity(StrEnum):
    """Severity of a dementia-care signal.

    Mirrors ``continuoustracking.v1.DementiaSignalSeverity`` (values 1..3).
    """

    INFO = "info"
    WARNING = "warning"
    EMERGENCY = "emergency"

    @classmethod
    def from_wire(cls, value: str) -> DementiaSignalSeverity | None:
        try:
            return cls(value)
        except ValueError:
            return None

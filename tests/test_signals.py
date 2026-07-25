"""Tests for the canonical dementia-signal vocabulary."""

from __future__ import annotations

from cts_contracts import DementiaSignalKind, DementiaSignalSeverity


def test_kind_members_match_wire_strings() -> None:
    # The exact wire vocabulary (proto enum values 1..10), in order.
    assert [k.value for k in DementiaSignalKind] == [
        "pacing",
        "sundowning_index",
        "bathroom_dwell_anomaly",
        "nighttime_movement",
        "stillness_anomaly",
        "absence",
        "fall_suspected",
        "gait_slowing",
        "agitation_index",
        "same_clothes_suspected",
    ]


def test_strenum_compares_equal_to_plain_string() -> None:
    # Migration safety: existing `== "stillness_anomaly"` comparisons keep working.
    assert DementiaSignalKind.STILLNESS_ANOMALY == "stillness_anomaly"
    assert DementiaSignalSeverity.WARNING == "warning"


def test_from_wire_parses_known_and_rejects_unknown() -> None:
    assert DementiaSignalKind.from_wire("absence") is DementiaSignalKind.ABSENCE
    assert DementiaSignalKind.from_wire("not_a_kind") is None
    assert DementiaSignalSeverity.from_wire("emergency") is DementiaSignalSeverity.EMERGENCY
    assert DementiaSignalSeverity.from_wire("nope") is None


def test_severity_members() -> None:
    assert [s.value for s in DementiaSignalSeverity] == ["info", "warning", "emergency"]

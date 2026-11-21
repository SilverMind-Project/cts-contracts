"""Tests for canonical household presence vocabulary."""

from __future__ import annotations

from cts_contracts import PresenceStatus
from cts_contracts.household import PresenceStatus as HouseholdPresenceStatus

# Expected proto enum member names in continuoustracking/v1/household.proto
# (excluding PRESENCE_STATUS_UNSPECIFIED = 0).
_EXPECTED_PROTO_ENUM_NAMES = [
    "PRESENCE_STATUS_PRESENT_ROOM",
    "PRESENCE_STATUS_PRESENT_HOME",
    "PRESENCE_STATUS_AWAY",
    "PRESENCE_STATUS_ASLEEP",
    "PRESENCE_STATUS_UNKNOWN",
    "PRESENCE_STATUS_STALE",
]


def test_presence_status_reexport_is_single_class() -> None:
    assert PresenceStatus is HouseholdPresenceStatus


def test_presence_status_members_match_wire_strings() -> None:
    assert [m.value for m in PresenceStatus] == [
        "present_room",
        "present_home",
        "away",
        "asleep",
        "unknown",
        "stale",
    ]
    assert PresenceStatus.PRESENT_ROOM == "present_room"
    assert PresenceStatus.AWAY == "away"
    assert PresenceStatus.from_wire("asleep") is PresenceStatus.ASLEEP
    assert PresenceStatus.from_wire("on_vacation") is None


def test_presence_status_members_match_proto_enum_names() -> None:
    proto_names = [f"PRESENCE_STATUS_{m.name}" for m in PresenceStatus]
    assert proto_names == _EXPECTED_PROTO_ENUM_NAMES

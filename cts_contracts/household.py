"""Canonical household presence vocabulary shared across the platform.

These string values ARE the wire, storage, and in-process vocabulary shared by
``cognitive-companion`` (``PresenceService`` and ``HouseholdPresencePublisher``)
and ``continuous-tracking`` (``HouseholdPresenceSubscriber`` and
``ClosedWorldChannel``).

Members mirror the proto enum ``continuoustracking.v1.PresenceStatus`` in
``continuoustracking/v1/household.proto`` (lowercased, ``PRESENCE_STATUS_``
prefix-stripped; ``UNSPECIFIED`` = 0 is intentionally omitted because it is
never a valid emitted status).
"""

from __future__ import annotations

from enum import StrEnum


class PresenceStatus(StrEnum):
    """Current presence status of a household member.

    Mirrors ``continuoustracking.v1.PresenceStatus`` (values 1..6;
    ``PRESENCE_STATUS_UNSPECIFIED`` = 0 is intentionally omitted).
    """

    PRESENT_ROOM = "present_room"
    PRESENT_HOME = "present_home"
    AWAY = "away"
    ASLEEP = "asleep"
    UNKNOWN = "unknown"
    STALE = "stale"

    @classmethod
    def from_wire(cls, value: str) -> PresenceStatus | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None

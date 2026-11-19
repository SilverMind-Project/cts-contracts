"""Canonical wearable and RF-node vocabularies shared across the platform.

These string values ARE the wire, storage, and configuration vocabulary shared by
``continuous-tracking`` (``tracking-orchestrator`` and ``rf-ingress``) and
``cognitive-companion``. The six proto-backed enums mirror the enum names
(lowercased, prefix-stripped) in ``continuoustracking/v1/wearable.proto``.

Consumers branch on declared capabilities and covariance, never on hardware
vendor or product identity.
"""

from __future__ import annotations

from enum import StrEnum


class FixKind(StrEnum):
    """Kind of wearable localization fix on ``wearable.fixes``.

    Mirrors ``continuoustracking.v1.FixKind`` (values 1..3; ``UNSPECIFIED`` = 0
    is intentionally omitted because it is never a valid emitted fix kind).
    """

    POSITION = "position"
    ROOM = "room"
    PROXIMITY = "proximity"

    @classmethod
    def from_wire(cls, value: str) -> FixKind | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class AdapterKind(StrEnum):
    """Hardware-neutral RF adapter family declared in ``AdapterCapability``.

    Mirrors ``continuoustracking.v1.AdapterKind`` (values 1..5; ``UNSPECIFIED`` = 0
    is intentionally omitted).
    """

    DEVICE_RANGING = "device_ranging"
    ANCHOR_RANGING = "anchor_ranging"
    SOLVED_POSITION = "solved_position"
    ROOM_PRESENCE = "room_presence"
    SIMULATOR = "simulator"

    @classmethod
    def from_wire(cls, value: str) -> AdapterKind | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class WearState(StrEnum):
    """Whether a wearable device reports being worn on the body.

    Mirrors ``continuoustracking.v1.WearState`` (values 0..2). ``UNSPECIFIED``
    is a valid runtime wire value for devices (such as coin-cell beacons) that
    cannot determine on-body state.
    """

    UNSPECIFIED = "unspecified"
    ON_BODY = "on_body"
    OFF_BODY = "off_body"

    @classmethod
    def from_wire(cls, value: str) -> WearState | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class MotionState(StrEnum):
    """Whether a wearable tag is currently moving or stationary.

    Mirrors ``continuoustracking.v1.MotionState`` (values 0..2). ``UNSPECIFIED``
    is a valid runtime wire value when the adapter cannot determine motion state.
    """

    UNSPECIFIED = "unspecified"
    MOVING = "moving"
    STILL = "still"

    @classmethod
    def from_wire(cls, value: str) -> MotionState | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class RfNodeRole(StrEnum):
    """Role of a fixed RF node registered in Cognitive Companion.

    Mirrors ``continuoustracking.v1.RfNodeRole`` (values 1..2; ``UNSPECIFIED`` = 0
    is intentionally omitted).
    """

    RECEIVER = "receiver"
    RANGING_ANCHOR = "ranging_anchor"

    @classmethod
    def from_wire(cls, value: str) -> RfNodeRole | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class RangingTechnology(StrEnum):
    """Hardware-neutral RF localization technology declared by an adapter or RF node.

    Mirrors ``continuoustracking.v1.RangingTechnology`` (values 1..3;
    ``UNSPECIFIED`` = 0 is intentionally omitted).
    """

    BLE_RSSI = "ble_rssi"
    BLE_CHANNEL_SOUNDING = "ble_channel_sounding"
    UWB = "uwb"

    @classmethod
    def from_wire(cls, value: str) -> RangingTechnology | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


class DeviceKind(StrEnum):
    """Form-factor class of a registered wearable device in Cognitive Companion."""

    BLE_BEACON = "ble_beacon"
    WATCH = "watch"
    UWB_TAG = "uwb_tag"

    @classmethod
    def from_wire(cls, value: str) -> DeviceKind | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None

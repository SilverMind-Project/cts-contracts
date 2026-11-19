"""Tests for canonical wearable and RF-node vocabularies."""

from __future__ import annotations

from cts_contracts import (
    AdapterKind,
    DeviceKind,
    FixKind,
    MotionState,
    RangingTechnology,
    RfNodeRole,
    WearState,
)


def test_fix_kind_members_match_wire_strings() -> None:
    assert [m.value for m in FixKind] == ["position", "room", "proximity"]
    assert FixKind.POSITION == "position"
    assert FixKind.from_wire("room") is FixKind.ROOM
    assert FixKind.from_wire("unknown") is None


def test_adapter_kind_members_match_wire_strings() -> None:
    assert [m.value for m in AdapterKind] == [
        "device_ranging",
        "anchor_ranging",
        "solved_position",
        "room_presence",
        "simulator",
    ]
    assert AdapterKind.SIMULATOR == "simulator"
    assert AdapterKind.from_wire("room_presence") is AdapterKind.ROOM_PRESENCE
    assert AdapterKind.from_wire("vendor_xyz") is None


def test_wear_state_members_match_wire_strings() -> None:
    assert [m.value for m in WearState] == ["unspecified", "on_body", "off_body"]
    assert WearState.ON_BODY == "on_body"
    assert WearState.from_wire("unspecified") is WearState.UNSPECIFIED
    assert WearState.from_wire("unknown") is None


def test_motion_state_members_match_wire_strings() -> None:
    assert [m.value for m in MotionState] == ["unspecified", "moving", "still"]
    assert MotionState.MOVING == "moving"
    assert MotionState.from_wire("still") is MotionState.STILL
    assert MotionState.from_wire("running") is None


def test_rf_node_role_members_match_wire_strings() -> None:
    assert [m.value for m in RfNodeRole] == ["receiver", "ranging_anchor"]
    assert RfNodeRole.RECEIVER == "receiver"
    assert RfNodeRole.from_wire("ranging_anchor") is RfNodeRole.RANGING_ANCHOR
    assert RfNodeRole.from_wire("beacon") is None


def test_ranging_technology_members_match_wire_strings() -> None:
    assert [m.value for m in RangingTechnology] == ["ble_rssi", "ble_channel_sounding", "uwb"]
    assert RangingTechnology.UWB == "uwb"
    assert RangingTechnology.from_wire("ble_channel_sounding") is (
        RangingTechnology.BLE_CHANNEL_SOUNDING
    )
    assert RangingTechnology.from_wire("wifi") is None


def test_device_kind_members_match_wire_strings() -> None:
    assert [m.value for m in DeviceKind] == ["ble_beacon", "watch", "uwb_tag"]
    assert DeviceKind.BLE_BEACON == "ble_beacon"
    assert DeviceKind.from_wire("uwb_tag") is DeviceKind.UWB_TAG
    assert DeviceKind.from_wire("tag") is None

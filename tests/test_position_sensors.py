"""Tests for the position-sensor vocabulary and source-id format."""

from __future__ import annotations

import pytest

from cts_contracts import (
    DEVICE_FREE_SOURCE_PREFIX,
    PositionSensorModality,
    is_device_free_source,
    is_valid_sensor_id,
    sensor_id_from_source,
    source_id_for_sensor,
)


def test_source_id_round_trips() -> None:
    source_id = source_id_for_sensor("radar-bathroom-1")
    assert source_id == "sensor:radar-bathroom-1"
    assert source_id.startswith(DEVICE_FREE_SOURCE_PREFIX)
    assert sensor_id_from_source(source_id) == "radar-bathroom-1"
    assert is_device_free_source(source_id)


@pytest.mark.parametrize(
    "camera_id",
    ["living-room-2", "cam_hallway", "", "sensor", "sensor:", "sensor:Radar", "sensor:a:b"],
)
def test_camera_ids_and_malformed_source_ids_are_not_device_free(camera_id: str) -> None:
    assert sensor_id_from_source(camera_id) is None
    assert not is_device_free_source(camera_id)


@pytest.mark.parametrize(
    ("sensor_id", "valid"),
    [
        ("radar-bathroom-1", True),
        ("lidar.living_0", True),
        ("0", True),
        ("a" * 64, True),
        ("a" * 65, False),
        ("", False),
        ("-radar", False),
        ("Radar", False),
        ("radar bathroom", False),
        ("sensor:radar", False),
    ],
)
def test_sensor_id_slug(sensor_id: str, valid: bool) -> None:
    assert is_valid_sensor_id(sensor_id) is valid


def test_source_id_for_invalid_sensor_id_raises() -> None:
    with pytest.raises(ValueError, match="invalid position sensor id"):
        source_id_for_sensor("Not A Slug")


def test_modality_wire_values() -> None:
    assert [m.value for m in PositionSensorModality] == ["mmwave_radar", "lidar", "other"]
    assert PositionSensorModality.from_wire("lidar") is PositionSensorModality.LIDAR
    assert PositionSensorModality.from_wire("sonar") is None

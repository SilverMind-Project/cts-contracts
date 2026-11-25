"""Vocabulary for device-free anonymous position sensors (mmWave radar, 2D/3D LiDAR).

A position sensor reports anonymous floor-plane tracks (``AnonymousPositionTrack`` on
``position.tracks``) and never carries identity. ``cognitive-companion`` owns the sensor
registry; ``continuous-tracking`` feeds the tracks to the world tracker.

Inside the tracker a sensor plays the part a camera plays for its detections, so its
observations, persisted rows, and published ``TrackingEvent``s carry a *source id* in the
``camera_id`` slot. The source id is ``sensor:<sensor_id>``. Building and parsing that id
happens only through this module, so the producer (``tracking-orchestrator``) and the
consumer (``cognitive-companion``) can never disagree on its format. The ``:`` separator
cannot occur in a sensor id or a camera id slug, so a source id never collides with a
camera id.
"""

from __future__ import annotations

import re
from enum import StrEnum
from typing import Final

DEVICE_FREE_SOURCE_PREFIX: Final[str] = "sensor:"
"""Prefix of the source id that stands in for a camera id for a position sensor."""

SENSOR_ID_PATTERN: Final[str] = r"^[a-z0-9][a-z0-9_.-]{0,63}$"
"""A sensor id: a lowercase slug of 1 to 64 characters with no ``:``."""

_SENSOR_ID_RE: Final[re.Pattern[str]] = re.compile(SENSOR_ID_PATTERN)


class PositionSensorModality(StrEnum):
    """What kind of device-free sensor a registered position sensor is.

    Display and inventory only: consumers branch on the reported covariance, never on
    the modality, exactly as wearable consumers never branch on the radio.
    """

    MMWAVE_RADAR = "mmwave_radar"
    LIDAR = "lidar"
    OTHER = "other"

    @classmethod
    def from_wire(cls, value: str) -> PositionSensorModality | None:
        """Parse a wire/stored string into a member, or ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None


def is_valid_sensor_id(sensor_id: str) -> bool:
    """Return whether *sensor_id* is a well-formed sensor id slug."""
    return bool(_SENSOR_ID_RE.fullmatch(sensor_id))


def source_id_for_sensor(sensor_id: str) -> str:
    """Return the source id (``sensor:<sensor_id>``) that stands in for a camera id.

    Raises:
        ValueError: *sensor_id* is not a valid sensor id slug.
    """
    if not is_valid_sensor_id(sensor_id):
        raise ValueError(f"invalid position sensor id: {sensor_id!r}")
    return f"{DEVICE_FREE_SOURCE_PREFIX}{sensor_id}"


def sensor_id_from_source(source_id: str) -> str | None:
    """Return the sensor id of a device-free source id, or ``None`` for any other id.

    A camera id, an empty string, or a malformed ``sensor:`` id all return ``None``.
    """
    if not source_id.startswith(DEVICE_FREE_SOURCE_PREFIX):
        return None
    sensor_id = source_id[len(DEVICE_FREE_SOURCE_PREFIX) :]
    return sensor_id if is_valid_sensor_id(sensor_id) else None


def is_device_free_source(source_id: str) -> bool:
    """Return whether *source_id* names a position sensor rather than a camera."""
    return sensor_id_from_source(source_id) is not None

"""Canonical camera-role vocabulary shared across the Continuous Tracking platform.

These string values are stored in Cognitive Companion's ``cts_cameras.role`` column and
synced into the tracking orchestrator's ``CameraProfile`` map. Consumers branch on declared
role and capability, never on camera vendor or model.
"""

from __future__ import annotations

from enum import StrEnum


class CameraRole(StrEnum):
    """Operational role of a CTS camera.

    ``face_capable`` designates an identification-point camera (face-first, short face-ID
    cooldown; requires floor calibration to attach faces to shared person hypotheses).
    ``mixed`` and ``surveillance`` use the standard face-ID cooldown. Role never disables
    face identification on its own; ``face_id_enabled`` is the per-camera switch.
    """

    FACE_CAPABLE = "face_capable"
    SURVEILLANCE = "surveillance"
    MIXED = "mixed"

    @classmethod
    def from_wire(cls, value: str) -> CameraRole | None:
        """Parse a wire/stored role string, or return ``None`` if unknown."""
        try:
            return cls(value)
        except ValueError:
            return None

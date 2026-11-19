"""Shared wire-contract datatypes and pure helpers for the Continuous Tracking platform.

This package is the single source of truth for the *hand-written* contract types and pure
helpers shared between the producer (``continuous-tracking/tracking-orchestrator``) and the
consumer (``cognitive-companion``): the canonical dementia-signal vocabulary, camera roles,
and pinhole optics helpers. It deliberately has no protobuf dependency so either side can
adopt it without pulling the generated SDK.

The generated protobuf bindings (``continuoustracking.v1.*_pb2``) are a separate,
heavier concern; see ``README.md`` for the two-problem strategy and migration plan.
"""

from __future__ import annotations

from cts_contracts.cameras import CameraRole
from cts_contracts.optics import (
    ADULT_MEAN_INTERPUPILLARY_M,
    INTEROCULAR_BANDS_PX,
    INTEROCULAR_GOOD_MIN_PX,
    InterocularBand,
    InterocularBandSpec,
    classify_interocular_px,
    distance_for_interocular_m,
    expected_interocular_px,
    focal_length_px,
)
from cts_contracts.signals import (
    DementiaSignalKind,
    DementiaSignalSeverity,
)
from cts_contracts.wearables import (
    AdapterKind,
    DeviceKind,
    FixKind,
    MotionState,
    RangingTechnology,
    RfNodeRole,
    WearState,
)

__all__ = [
    "ADULT_MEAN_INTERPUPILLARY_M",
    "INTEROCULAR_BANDS_PX",
    "INTEROCULAR_GOOD_MIN_PX",
    "AdapterKind",
    "CameraRole",
    "DementiaSignalKind",
    "DementiaSignalSeverity",
    "DeviceKind",
    "FixKind",
    "InterocularBand",
    "InterocularBandSpec",
    "MotionState",
    "RangingTechnology",
    "RfNodeRole",
    "WearState",
    "classify_interocular_px",
    "distance_for_interocular_m",
    "expected_interocular_px",
    "focal_length_px",
]

__version__ = "0.3.0"

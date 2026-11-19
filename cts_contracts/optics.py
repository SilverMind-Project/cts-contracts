"""Pinhole camera optics helpers shared by tracking-orchestrator and cognitive-companion.

Pure standard-library math only. Every function uses the rectilinear pinhole camera model
(no radial or tangential lens distortion); wide-angle lenses (above roughly 110 degrees
horizontal FOV) have barrel distortion at image edges, so these estimates are documented
approximations intended for placement planning and single-view geometry calculations.

Units are carried in every parameter and function name: pixels (``_px``), degrees
(``_deg``), and metres (``_m``).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Final, Literal

# Mean adult interpupillary distance in metres (63 mm).
ADULT_MEAN_INTERPUPILLARY_M: Final[float] = 0.063

# Target interocular pixel threshold for reliable face recognition ("good" band floor).
INTEROCULAR_GOOD_MIN_PX: Final[float] = 24.0

InterocularBand = Literal["poor", "marginal", "good", "excellent"]


@dataclass(frozen=True)
class InterocularBandSpec:
    """Inclusive-lower, exclusive-upper interocular distance band in pixels."""

    band: InterocularBand
    min_px: float | None
    max_px: float | None


# Canonical interocular pixel quality bands shared across backend optics endpoints, UI
# placement calculators, and documentation.
INTEROCULAR_BANDS_PX: Final[tuple[InterocularBandSpec, ...]] = (
    InterocularBandSpec(band="poor", min_px=None, max_px=16.0),
    InterocularBandSpec(band="marginal", min_px=16.0, max_px=24.0),
    InterocularBandSpec(band="good", min_px=24.0, max_px=40.0),
    InterocularBandSpec(band="excellent", min_px=40.0, max_px=None),
)


def _require_positive_finite(value: float, name: str) -> float:
    val = float(value)
    if not math.isfinite(val) or val <= 0.0:
        raise ValueError(f"{name} must be finite and > 0, got {value!r}")
    return val


def focal_length_px(width_px: int | float, hfov_deg: float) -> float:
    """Return horizontal focal length in pixels under the pinhole approximation.

    Assumes a rectilinear lens (no distortion) with principal point at the image centre:
    ``focal_px = (width_px / 2) / tan(radians(hfov_deg) / 2)``.

    Args:
        width_px: Stream image width in pixels (must be > 0).
        hfov_deg: Horizontal field of view in degrees, strictly in ``(0, 180)``.

    Returns:
        Derived horizontal focal length in pixels.
    """
    w = _require_positive_finite(width_px, "width_px")
    fov = float(hfov_deg)
    if not math.isfinite(fov) or fov <= 0.0 or fov >= 180.0:
        raise ValueError(f"hfov_deg must be finite and in (0, 180), got {hfov_deg!r}")
    return (w / 2.0) / math.tan(math.radians(fov) / 2.0)


def expected_interocular_px(
    focal_px: float,
    distance_m: float,
    iod_m: float = ADULT_MEAN_INTERPUPILLARY_M,
) -> float:
    """Return expected interocular distance in pixels at ``distance_m`` metres.

    Uses the pinhole approximation for a frontal face perpendicular to the optical axis:
    ``iod_px = focal_px * iod_m / distance_m``.

    Args:
        focal_px: Horizontal focal length in pixels (from :func:`focal_length_px`).
        distance_m: Distance from the camera lens to the face in metres (> 0).
        iod_m: Physical interpupillary distance in metres (default 0.063 m adult mean).

    Returns:
        Expected interocular span in pixels.
    """
    f = _require_positive_finite(focal_px, "focal_px")
    d = _require_positive_finite(distance_m, "distance_m")
    iod = _require_positive_finite(iod_m, "iod_m")
    return f * iod / d


def distance_for_interocular_m(
    focal_px: float,
    target_px: float,
    iod_m: float = ADULT_MEAN_INTERPUPILLARY_M,
) -> float:
    """Return the distance in metres at which a face spans ``target_px`` interocular pixels.

    Exact inverse of :func:`expected_interocular_px` under the pinhole approximation:
    ``distance_m = focal_px * iod_m / target_px``.

    Args:
        focal_px: Horizontal focal length in pixels (from :func:`focal_length_px`).
        target_px: Desired interocular distance in pixels (> 0).
        iod_m: Physical interpupillary distance in metres (default 0.063 m adult mean).

    Returns:
        Maximum distance in metres to achieve ``target_px`` interocular pixels.
    """
    f = _require_positive_finite(focal_px, "focal_px")
    t = _require_positive_finite(target_px, "target_px")
    iod = _require_positive_finite(iod_m, "iod_m")
    return f * iod / t


def classify_interocular_px(iod_px: float) -> InterocularBand:
    """Classify an interocular pixel span into one of :data:`INTEROCULAR_BANDS_PX`."""
    val = float(iod_px)
    if not math.isfinite(val) or val < 0.0:
        raise ValueError(f"iod_px must be finite and >= 0, got {iod_px!r}")
    for spec in INTEROCULAR_BANDS_PX:
        lower_ok = spec.min_px is None or val >= spec.min_px
        upper_ok = spec.max_px is None or val < spec.max_px
        if lower_ok and upper_ok:
            return spec.band
    return "excellent"

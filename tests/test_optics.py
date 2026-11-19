"""Tests for pinhole camera optics helpers and the shared camera role vocabulary."""

from __future__ import annotations

import math

import pytest

from cts_contracts import (
    ADULT_MEAN_INTERPUPILLARY_M,
    INTEROCULAR_BANDS_PX,
    INTEROCULAR_GOOD_MIN_PX,
    CameraRole,
    classify_interocular_px,
    distance_for_interocular_m,
    expected_interocular_px,
    focal_length_px,
)


class TestOptics:
    def test_2560px_at_90deg_matches_pinhole_reference(self) -> None:
        focal = focal_length_px(2560, 90.0)
        assert math.isclose(focal, 1280.0, rel_tol=1e-9)
        iod_at_2m = expected_interocular_px(focal, 2.0)
        assert abs(iod_at_2m - 40.32) < 0.05
        assert abs(iod_at_2m - 40.0) < 1.0

    def test_2560px_at_110deg_matches_options_table(self) -> None:
        focal = focal_length_px(2560, 110.0)
        iod_at_2m = expected_interocular_px(focal, 2.0)
        # 2560 px at 110 deg yields ~28.23 px at 2 m (options report: ~28 px, within 1 px).
        assert abs(iod_at_2m - 28.0) < 1.0

    @pytest.mark.parametrize(
        ("width_px", "hfov_deg", "distance_m"),
        [
            (1280, 70.0, 1.5),
            (1920, 87.0, 2.5),
            (2560, 90.0, 3.0),
            (2560, 103.0, 4.0),
            (3840, 110.0, 5.0),
        ],
    )
    def test_distance_for_interocular_inverts_expected_interocular(
        self, width_px: int, hfov_deg: float, distance_m: float
    ) -> None:
        focal = focal_length_px(width_px, hfov_deg)
        iod_px = expected_interocular_px(focal, distance_m)
        recovered_m = distance_for_interocular_m(focal, iod_px)
        assert math.isclose(recovered_m, distance_m, rel_tol=1e-12)

    def test_custom_iod_round_trip(self) -> None:
        focal = focal_length_px(2560, 60.0)
        iod_px = expected_interocular_px(focal, 2.0, iod_m=0.060)
        assert math.isclose(distance_for_interocular_m(focal, iod_px, iod_m=0.060), 2.0)
        assert ADULT_MEAN_INTERPUPILLARY_M == 0.063
        assert INTEROCULAR_GOOD_MIN_PX == 24.0

    def test_interocular_bands_and_classification(self) -> None:
        assert [spec.band for spec in INTEROCULAR_BANDS_PX] == [
            "poor",
            "marginal",
            "good",
            "excellent",
        ]
        assert classify_interocular_px(0.0) == "poor"
        assert classify_interocular_px(15.99) == "poor"
        assert classify_interocular_px(16.0) == "marginal"
        assert classify_interocular_px(23.99) == "marginal"
        assert classify_interocular_px(24.0) == "good"
        assert classify_interocular_px(39.99) == "good"
        assert classify_interocular_px(40.0) == "excellent"
        assert classify_interocular_px(80.0) == "excellent"

    @pytest.mark.parametrize(
        ("width_px", "hfov_deg"),
        [
            (0, 90.0),
            (-100, 90.0),
            (2560, 0.0),
            (2560, -10.0),
            (2560, 180.0),
            (2560, 200.0),
            (2560, float("nan")),
            (2560, float("inf")),
        ],
    )
    def test_focal_length_rejects_invalid_inputs(self, width_px: int, hfov_deg: float) -> None:
        with pytest.raises(ValueError):
            focal_length_px(width_px, hfov_deg)

    def test_expected_and_distance_reject_non_positive(self) -> None:
        with pytest.raises(ValueError):
            expected_interocular_px(0.0, 2.0)
        with pytest.raises(ValueError):
            expected_interocular_px(1280.0, 0.0)
        with pytest.raises(ValueError):
            expected_interocular_px(1280.0, 2.0, iod_m=-0.01)
        with pytest.raises(ValueError):
            distance_for_interocular_m(1280.0, 0.0)
        with pytest.raises(ValueError):
            classify_interocular_px(-1.0)


class TestCameraRole:
    def test_role_members(self) -> None:
        assert [r.value for r in CameraRole] == ["face_capable", "surveillance", "mixed"]

    def test_from_wire(self) -> None:
        assert CameraRole.from_wire("face_capable") is CameraRole.FACE_CAPABLE
        assert CameraRole.from_wire("surveillance") is CameraRole.SURVEILLANCE
        assert CameraRole.from_wire("mixed") is CameraRole.MIXED
        assert CameraRole.from_wire("identification_point") is None
        assert CameraRole.from_wire("") is None

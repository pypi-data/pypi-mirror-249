import pytest
from arrayscaler.arrayscaler import ScalingHelper


def test_scale() -> None:
    assert ScalingHelper.scale(5, 0, 10) == 0.5
    assert ScalingHelper.scale(0, 0, 10) == 0
    assert ScalingHelper.scale(10, 0, 10) == 1


def test_rescale() -> None:
    assert ScalingHelper.rescale(0.5, 0, 10) == 5
    assert ScalingHelper.rescale(0, 0, 10) == 0
    assert ScalingHelper.rescale(1, 0, 10) == 10


if __name__ == "__main__":
    pytest.main([__file__])

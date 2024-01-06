import numpy as np
import pytest
from arrayscaler.arrayscaler import ScalingHelper


def test_scale() -> None:
    assert ScalingHelper.scale(5, 0, 10) == 0.5
    assert ScalingHelper.scale(0, 0, 10) == 0
    assert ScalingHelper.scale(10, 0, 10) == 1
    assert np.allclose(
        ScalingHelper.scale(np.array([1, 3, 4, 5, 3, 2]), 0, 2),
        np.array([0.5, 1.5, 2, 2.5, 1.5, 1]),
    )
    assert np.allclose(
        ScalingHelper.scale(np.array([0, 1, 2, 3, 4, 5]), 0, 5),
        np.array([0, 0.2, 0.4, 0.6, 0.8, 1]),
    )


def test_rescale() -> None:
    assert ScalingHelper.rescale(0.5, 0, 10) == 5
    assert ScalingHelper.rescale(0, 0, 10) == 0
    assert ScalingHelper.rescale(1, 0, 10) == 10
    assert np.allclose(
        ScalingHelper.rescale(np.array([0.5, 1.5, 2, 2.5, 1.5, 1]), 0, 2),
        np.array([1, 3, 4, 5, 3, 2]),
    )
    assert np.allclose(
        ScalingHelper.rescale(np.array([0, 0.2, 0.4, 0.6, 0.8, 1]), 0, 5),
        np.array([0, 1, 2, 3, 4, 5]),
    )


def test_invalid_input() -> None:
    with pytest.raises(TypeError):
        ScalingHelper.scale("invalid", 0, 10)


if __name__ == "__main__":
    pytest.main([__file__])

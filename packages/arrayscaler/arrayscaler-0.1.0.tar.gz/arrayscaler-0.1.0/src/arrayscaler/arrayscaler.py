import numpy as np


class ScalingHelper:
    """A class that provides methods for scaling and rescaling values."""

    @staticmethod
    def scale(d: np.ndarray | float, d_min: float, d_max: float) -> np.ndarray | float:
        """
        Scales a value between 0 and 1 based on the given minimum and maximum values.

        Args:
        ----
            d (float): The value to be scaled.
            d_min (float): The minimum value of the range.
            d_max (float): The maximum value of the range.

        Returns:
        -------
            float: The scaled value between 0 and 1.
        """
        # ensure that the values has the same decimal precision
        scaled_d = (d - d_min) / ((d_max - d_min) + 1e-10)
        # ROUND THE VALUE TO 4 DECIMAL PLACES
        scaled_d = np.round(scaled_d, 4)
        return scaled_d

    @staticmethod
    def rescale(
        d: np.ndarray | float, d_min: float, d_max: float
    ) -> np.ndarray | float:
        """
        Rescales a value between the given minimum
        and maximum values to its original range.

        Args:
        ----
            d (float): The value to be rescaled.
            d_min (float): The minimum value of the range.
            d_max (float): The maximum value of the range.

        Returns:
        -------
            float: The rescaled value between d_min and d_max.
        """
        rescaled_d = d_min + (d_max - d_min) * d
        return rescaled_d

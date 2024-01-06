import numpy as np


class ScalingHelper:
    """A class that provides methods for scaling and rescaling values."""

    @staticmethod
    def scale(
        d: np.ndarray | float | int | list,
        d_min: float | None = None,
        d_max: float | None = None,
    ) -> np.ndarray | float:
        """
        Scales a value between 0 and 1 based on
        the given minimum and maximum values.
        If no minimum and maximum values are provided,
        they are calculated from the input data.

        Args:
        ----
            d (float | int | list): The value to be scaled.
            If int or list, it will be converted to float or np array.
            d_min (float, optional): The minimum value of the range. Defaults to None.
            d_max (float, optional): The maximum value of the range. Defaults to None.

        Returns:
        -------
            float: The scaled value between 0 and 1.
        """
        if isinstance(d, list):
            d = np.array(d, dtype=float)
        elif isinstance(d, int):
            d = float(d)
        elif not isinstance(d, float | np.ndarray):
            raise TypeError("Input data must be a float, int, list or a numpy array.")
        if d_min is None:
            d_min = np.min(d)
        if d_max is None:
            d_max = np.max(d)
        scaled_d = (d - d_min) / ((d_max - d_min) + 1e-10)
        scaled_d = np.round(scaled_d, 4)
        return scaled_d

    @staticmethod
    def rescale(
        d: np.ndarray | float | int | list,
        d_min: float | None = None,
        d_max: float | None = None,
    ) -> np.ndarray | float:
        """
        Rescales a value between the given minimum
        and maximum values to its original range.
        If no minimum and maximum values are provided,
        they are calculated from the input data.

        Args:
        ----
            d (float | int | list): The value to be rescaled.
            If int or list, it will be converted to float or np array.
            d_min (float, optional): The minimum value of the range. Defaults to None.
            d_max (float, optional): The maximum value of the range. Defaults to None.

        Returns:
        -------
            float: The rescaled value between d_min and d_max.
        """
        if isinstance(d, list):
            d = np.array(d, dtype=float)
        elif isinstance(d, int):
            d = float(d)
        elif not isinstance(d, float | np.ndarray):
            raise TypeError("Input data must be a float, int, list or a numpy array.")
        if d_min is None:
            d_min = np.min(d)
        if d_max is None:
            d_max = np.max(d)
        rescaled_d = d_min + (d_max - d_min) * d
        return rescaled_d

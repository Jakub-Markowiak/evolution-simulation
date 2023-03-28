import numpy as np


class RGB:
    """
    Color representation using RGB model.

    Parameters:
        red (int): red color saturation (value between 0 and 255)
        green (int): green color saturation (value between 0 and 255)
        blue (int): blue color saturation (value between 0 and 255)
    """

    def __init__(self, red: int, green: int, blue: int) -> None:
        assert all(
            {0 <= value <= 255 for value in {red, green, blue}}
        ), "color values must be between 0 and 255 (inclusively)"
        self.code = (int(red), int(green), int(blue))

    def __repr__(self) -> str:
        return f"RGB: {self.code}"

    def calculate_similarity(self, other: "RGB") -> float:
        """
        Calculate similarity between pair of RGB objects using eucliden distance for R^3 space.
        Returns similarity level (value from [0,1]).

        Parameters:
            other (RGB): other object to compare similarity with
        """
        _max_distance = (3 * 255**2) ** 0.5
        difference = (
            sum([(v_1 - v_2) ** 2 for v_1, v_2 in zip(self.code, other.code)]) ** 0.5
            / _max_distance
        )
        similarity = 1 - difference
        return similarity

    def generate_random() -> "RGB":
        """
        Generate random color.
        Returns RGB object with random values.
        """
        red, green, blue = np.random.randint(0, 255, 3)
        return RGB(red, green, blue)

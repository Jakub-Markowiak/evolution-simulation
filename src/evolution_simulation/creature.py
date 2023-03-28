from uuid import UUID, uuid4
from src.handlers.rgb import RGB

import numpy as np
import random


class Creature:
    """
    Creature class used for simulation purposes.

    Parameters:
        color (RGB): color assigned to creature
        position (tuple[float, float]): coordinates representing creature position
        mutant (bool): set to True if creature is considered mutant

    Attributes:
        uuid (UUID): unique identifier assigned during initalization
    """

    _allowed_methods = {"discrete", "mean"}

    def __init__(
        self, color: RGB, position: tuple[float, float] = None, mutant=False
    ) -> None:
        self.uuid = uuid4()
        self.color = color
        self.position = position
        self.is_mutant = mutant

    def __repr__(self) -> str:
        return f"Creature with uuid {self.uuid} and color {self.color}"

    def distance(self, other: "Creature") -> float:
        """
        Calculate distance from other creature using euclidean metric on R^2 space.
        """
        if (self.position is not None) and (other.position is not None):
            distance = sum(
                (v_1 - v_2) ** 2 for v_1, v_2 in zip(self.position, other.position)
            ) ** (0.5)
            return distance

        else:
            return None

    def breed(
        self,
        other: "Creature",
        min_color_similarity: float = 0,
        chance_mutant: float = 0,
        color_method: str = "discrete",
    ) -> "Creature":
        """
        Breed creatures if conditions are fulfilled.

        Parameters:
            other (Creature): other creature to breed with
            min_color_similarity (float): level of color similarity required to breed (value must be in [0,1])
            chance_mutant (float): chance that mutant borns (value must be in [0,1])
            color_method (str): new color assigment method, one of `(discrete, mean)`
        """
        assert all(
            {0 <= value <= 1 for value in {min_color_similarity, chance_mutant}}
        ), "value must be in [0, 1]"
        assert color_method in self._allowed_methods, "method is not handled"

        if self.color.calculate_similarity(other.color) < min_color_similarity:
            return
        else:
            pass

        is_mutant: bool = np.random.choice(
            [True, False], size=None, p=[chance_mutant, 1 - chance_mutant]
        )
        # Written in Python 3.9; no match/case syntax available yet
        if is_mutant:
            new_color = RGB.generate_random()
        elif color_method == "discrete":
            new_color = random.choice([self.color, other.color])
        elif color_method == "mean":
            params = tuple(
                np.round(np.mean([v_1, v_2]))
                for v_1, v_2 in zip(self.color.code, other.color.code)
            )
            new_color = RGB(*params)

        new_creature = Creature(color=new_color, mutant=is_mutant)
        return new_creature

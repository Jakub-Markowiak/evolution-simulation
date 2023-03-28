from .creature import Creature
from itertools import compress

import numpy as np


class Simulation:
    """
    Evolution simulation manager. Allows to perform experiments needed to generate data required in analysis. Change default parameters to adjust creatures behaviour for specific task.

    Parameters:
        size (tuple[int,int]): size `(rows, columns)`
        starting_creatures (iter[Creature]): set of starting creatures
        duration (int): number of iterations in simulation
        chance_death (float): chance of creature death in each iteration
        chance_breed (float): chance of creature breed in each iteration
        chance_mutant (float): chance of mutant birth
        min_color_similarity (float): minimum color similarity to breed
        view_distance (int): maximum distance between breeding creatures
    """

    def __init__(
        self,
        starting_creatures: list[Creature],
        size: float = 1000,
        view_distance: int = 250,
        color_method: str = "discrete",
        min_color_similarity: float = 0,
        duration: int = 100,
        chance_death: float = 0.1,
        chance_breed: float = 0.5,
        chance_mutant: float = 0,
    ) -> None:
        assert all(
            {
                0 <= value <= 1
                for value in {
                    chance_death,
                    chance_breed,
                    chance_mutant,
                    min_color_similarity,
                }
            }
        ), "value must be in [0,1]"
        assert all(
            {value >= 0 for value in {size, view_distance, duration}}
        ), "view distance must be positive"
        assert (
            color_method in Creature._allowed_methods
        ), "specified method is not handled"

        self.size = size
        self.creatures = np.array(starting_creatures, dtype=Creature)
        self.duration = duration
        self.chance_death = chance_death
        self.chance_breed = chance_breed
        self.chance_mutant = chance_mutant
        self.min_color_similarity = min_color_similarity
        self.view_distance = view_distance
        self.color_method = color_method

        self.run()

    def run(self):
        self._assign_position(self.creatures)
        self.history = list()
        i = 0
        while i < self.duration:
            self._simulate_day()
            self.history.append({"day": i, "count": len(self.creatures)})
            i += 1

    def _assign_position(self, creatures: list[Creature]):
        """
        Assign positions to creatures from specified list.
        """
        positions = np.random.uniform(0, self.size, (len(creatures), 2))
        for index, creature in enumerate(creatures):
            creature.position = positions[index]

    def _remove_position(self, creatures: list[Creature]):
        """
        Remove position for each creature from specified list.
        """
        for creature in creatures:
            creature.position = None

    def _simulate_day(self):
        """
        Simulate one day.
        """
        self._perform_deaths()
        self._perform_breeding()

    def _perform_deaths(self):
        """
        Calculate deaths in one iteration.
        """
        death_indicator = np.random.choice(
            [True, False],
            size=len(self.creatures),
            p=[self.chance_death, 1 - self.chance_death],
        )
        self._remove_position(self.creatures[death_indicator])
        self.creatures = self.creatures[~death_indicator]

    def _perform_breeding(self):
        """
        Perform breeding between creatures during the simulation step.
        """
        paired_creatures = self._pair_creatures()
        breed_indicator = np.random.choice(
            [True, False],
            size=int(len(self.creatures) / 2),
            p=[self.chance_breed, 1 - self.chance_breed],
        )

        breeding_creatures = compress(paired_creatures, breed_indicator)
        new_creatures = list()
        for (creature, pair) in breeding_creatures:
            if creature.distance(pair) <= self.view_distance:
                child = creature.breed(
                    other=pair,
                    min_color_similarity=self.min_color_similarity,
                    chance_mutant=self.chance_mutant,
                    color_method=self.color_method,
                )
                if child is not None:
                    new_creatures.append(child)

            else:
                pass

        self._assign_position(new_creatures)
        self.creatures = np.append(self.creatures, new_creatures)

    def _pair_creatures(self) -> dict[Creature:Creature]:
        """
        Randomly find a pair for each creature.
        """
        count_creatures = len(self.creatures)
        sampled_creatures = np.random.choice(
            self.creatures, size=count_creatures, replace=False
        )
        index = int(count_creatures / 2)
        pairs = zip(sampled_creatures[:index], sampled_creatures[index:])
        return pairs

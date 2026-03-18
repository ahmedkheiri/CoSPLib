"""
Created on Wed Mar 18 14:49:00 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from solution import Solution
from typing import List
import numpy as np
import config


class RandomNumberGenerator:
    def __init__(self) -> None:
        np.random.seed(config.SEED)

    def get_random_track_index(self, problem: Problem) -> int:
        return np.random.randint(problem.get_number_of_tracks())

    def get_two_random_session_indexes(self, problem: Problem) -> np.ndarray[np.long]:
        return np.random.randint(problem.get_number_of_sessions(), size=2)

    def get_two_random_room_indexes(self, problem: Problem) -> np.ndarray[np.long]:
        return np.random.randint(problem.get_number_of_rooms(), size=2)

    def get_two_random_submission_indexes(
        self, solution: Solution, track_index: int
    ) -> np.ndarray[np.long]:
        return np.random.randint(
            len(solution.get_submissions_indirect_solution()[track_index]), size=2
        )

    def get_random_integer(self, bound: int) -> int:
        return np.random.randint(bound)

    def shuffle_list(self, list: List) -> None:
        np.random.shuffle(list)

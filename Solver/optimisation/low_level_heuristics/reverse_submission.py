"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.random_number_generator import RandomNumberGenerator
from solution import Solution
from domain.problem import Problem


class ReverseSubmission:
    def __init__(self) -> None:
        self.__random: RandomNumberGenerator = RandomNumberGenerator()

    def apply(self, problem: Problem, solution: Solution) -> None:
        track = self.__random.get_random_track_index(problem)
        indexes = self.__random.get_two_random_submission_indexes(solution, track)
        this_index, other_index = indexes[0], indexes[1]
        while (this_index == other_index) or (
            len(solution.get_submissions_indirect_solution()[track]) == 1
        ):
            track = self.__random.get_random_track_index(problem)
            indexes = self.__random.get_two_random_submission_indexes(solution, track)
            this_index, other_index = indexes[0], indexes[1]
        sorted_indexes = sorted(indexes)
        this_index, other_index = sorted_indexes[0], sorted_indexes[1]
        temp: list = solution.get_submissions_indirect_solution()[track][
            this_index:other_index
        ]
        temp.reverse()
        solution.get_submissions_indirect_solution()[track][this_index:other_index] = (
            temp
        )

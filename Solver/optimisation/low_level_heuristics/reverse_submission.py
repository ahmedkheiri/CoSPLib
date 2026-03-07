"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from solution import Solution
from domain.problem import Problem
import numpy as np


class ReverseSubmission:
    def apply(self, problem: Problem, solution: Solution) -> None:
        track = np.random.randint(problem.get_number_of_tracks())
        indexes = np.random.randint(
            len(solution.get_submissions_indirect_solution()[track]), size=2
        )
        while (indexes[0] == indexes[1]) or (
            len(solution.get_submissions_indirect_solution()[track]) == 1
        ):
            track = np.random.randint(problem.get_number_of_tracks())
            indexes = np.random.randint(
                len(solution.get_submissions_indirect_solution()[track]), size=2
            )
        sorted_indexes = sorted(indexes)
        temp: list = solution.get_submissions_indirect_solution()[track][
            sorted_indexes[0] : sorted_indexes[1]
        ]
        temp.reverse()
        solution.get_submissions_indirect_solution()[track][
            sorted_indexes[0] : sorted_indexes[1]
        ] = temp

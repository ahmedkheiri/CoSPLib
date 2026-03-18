"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.random_number_generator import RandomNumberGenerator
from solution import Solution
from domain.problem import Problem


class SwapSubmission:
    def __init__(self) -> None:
        self.__random: RandomNumberGenerator = RandomNumberGenerator()

    def apply(self, problem: Problem, solution: Solution) -> None:
        track = self.__random.get_random_track_index(problem)
        submissions = self.__random.get_two_random_submission_indexes(solution, track)
        this_submission, other_submission = submissions[0], submissions[1]
        while (this_submission == other_submission) or (
            len(solution.get_submissions_indirect_solution()[track]) == 1
        ):
            track = self.__random.get_random_track_index(problem)
            submissions = self.__random.get_two_random_submission_indexes(
                solution, track
            )
            this_submission, other_submission = submissions[0], submissions[1]
        (
            solution.get_submissions_indirect_solution()[track][this_submission],
            solution.get_submissions_indirect_solution()[track][other_submission],
        ) = (
            solution.get_submissions_indirect_solution()[track][other_submission],
            solution.get_submissions_indirect_solution()[track][this_submission],
        )

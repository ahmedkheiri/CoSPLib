"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from solution import Solution
from domain.problem import Problem
import numpy as np


class SwapSubmission:
    def apply(self, problem: Problem, solution: Solution) -> None:
        track = np.random.randint(problem.get_number_of_tracks())
        subs = np.random.randint(len(solution.getIndSolSubmissions()[track]), size=2)
        while (subs[0] == subs[1]) or (
            len(solution.getIndSolSubmissions()[track]) == 1
        ):
            track = np.random.randint(problem.get_number_of_tracks())
            subs = np.random.randint(
                len(solution.getIndSolSubmissions()[track]), size=2
            )
        (
            solution.getIndSolSubmissions()[track][subs[0]],
            solution.getIndSolSubmissions()[track][subs[1]],
        ) = (
            solution.getIndSolSubmissions()[track][subs[1]],
            solution.getIndSolSubmissions()[track][subs[0]],
        )

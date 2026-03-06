"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from solution import Solution
from domain.problem import Problem
import numpy as np


class SwapTrack:
    def apply(self, problem: Problem, solution: Solution) -> None:
        if problem.get_number_of_tracks() == 1:
            return
        session = np.random.randint(problem.get_number_of_sessions(), size=2)
        room = np.random.randint(problem.get_number_of_rooms(), size=2)
        while (
            (session[0] == session[1] and room[0] == room[1])
            or (
                solution.get_tracks_solution()[session[0]][room[0]]
                + solution.get_tracks_solution()[session[1]][room[1]]
                == -2
            )
            or (
                solution.get_tracks_solution()[session[0]][room[0]]
                == solution.get_tracks_solution()[session[1]][room[1]]
            )
        ):
            session = np.random.randint(problem.get_number_of_sessions(), size=2)
            room = np.random.randint(problem.get_number_of_rooms(), size=2)
        (
            solution.get_tracks_solution()[session[0]][room[0]],
            solution.get_tracks_solution()[session[1]][room[1]],
        ) = (
            solution.get_tracks_solution()[session[1]][room[1]],
            solution.get_tracks_solution()[session[0]][room[0]],
        )

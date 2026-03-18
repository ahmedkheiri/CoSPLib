"""
Created on Wed Mar 4 15:44:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from optimisation.random_number_generator import RandomNumberGenerator
from solution import Solution
from domain.problem import Problem


class SwapTrack:
    def __init__(self) -> None:
        self.__random: RandomNumberGenerator = RandomNumberGenerator()

    def apply(self, problem: Problem, solution: Solution) -> None:
        if problem.get_number_of_tracks() == 1:
            return
        sessions = self.__random.get_two_random_session_indexes(problem)
        rooms = self.__random.get_two_random_room_indexes(problem)
        this_session, other_session = sessions[0], sessions[1]
        this_room, other_room = rooms[0], rooms[1]
        while (
            (this_session == other_session and this_room == other_room)
            or (
                solution.get_tracks_solution()[this_session][this_room]
                + solution.get_tracks_solution()[other_session][other_room]
                == -2
            )
            or (
                solution.get_tracks_solution()[this_session][this_room]
                == solution.get_tracks_solution()[other_session][other_room]
            )
        ):
            sessions = self.__random.get_two_random_session_indexes(problem)
            rooms = self.__random.get_two_random_room_indexes(problem)
            this_session, other_session = sessions[0], sessions[1]
            this_room, other_room = rooms[0], rooms[1]
        (
            solution.get_tracks_solution()[this_session][this_room],
            solution.get_tracks_solution()[other_session][other_room],
        ) = (
            solution.get_tracks_solution()[other_session][other_room],
            solution.get_tracks_solution()[this_session][this_room],
        )

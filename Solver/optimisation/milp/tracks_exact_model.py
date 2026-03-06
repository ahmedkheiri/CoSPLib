"""
Created on Thu Mar 5 11:11:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
import pandas as pd
from time import time
from solution import Solution
from typing import List, Dict
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, GUROBI
import logging


class TracksExactModel:
    def __init__(self, problem: Problem, solution: Solution) -> None:
        self.__problem: Problem = problem
        self.__solution: Solution = solution
        self.__model: LpProblem = LpProblem("TracksExactModel", LpMinimize)
        self.__variables: LpVariable = None
        self.__add_variables: LpVariable = None
        self.__add2_variables: LpVariable = None
        self.__penalties: LpVariable = None
        self.__names: List[str] = list()
        self.__sub_x_map: Dict[str, List[str]] = {
            problem.get_submission(submission).get_submission_name(): []
            for submission in range(problem.get_number_of_submissions())
            if problem.get_submission(submission).get_submission_required_time_slots()
            > 1
        }
        self.__track_session_room_x_map: Dict[str, List[str]] = {
            problem.get_track(track).get_track_name()
            + problem.get_session(session).get_session_name()
            + problem.get_room(room).get_room_name(): []
            for track in range(problem.get_number_of_tracks())
            for session in range(problem.get_number_of_sessions())
            for room in range(problem.get_number_of_rooms())
        }
        self.__add_names: List[str] = list()
        self.__track_z_map: Dict[str, List[str]] = {
            problem.get_track(track).get_track_name(): []
            for track in range(problem.get_number_of_tracks())
        }
        self.__session_room_z_map: Dict[str, List[str]] = dict()
        self.__room_track_z_map: Dict[str, List[str]] = {
            problem.get_room(room).get_room_name()
            + problem.get_track(track).get_track_name(): []
            for room in range(problem.get_number_of_rooms())
            for track in range(problem.get_number_of_tracks())
        }
        self.__track_session_room_z_map: Dict[str, str] = dict()
        self.__session_track_z_map: Dict[str, List[str]] = {
            problem.get_session(session).get_session_name()
            + problem.get_track(track).get_track_name(): []
            for session in range(problem.get_number_of_sessions())
            for track in range(problem.get_number_of_tracks())
        }
        self.__add2_names: List[str] = list()
        self.__track_room_y_map: Dict[str, str] = dict()
        self.__track_y_map: Dict[str, List[str]] = dict()
        self.__coefficients: Dict[str, int] = dict()
        self.__timeslots: Dict[str, int] = dict()
        self.__n: Dict[str, int] = dict()
        self.__mts_subs: List[int] = [
            submission
            for submission in range(problem.get_number_of_submissions())
            if problem.get_submission(submission).get_submission_required_time_slots()
            > 1
        ]
        self.__pen: List[str] = list()
        self.__build_decision_variables()
        self.__build_objective_function()
        self.__build_constraints()

    def solve(self, milp_time_limit_in_sec: int) -> None:
        logging.info("Solving with tracks exact milp model...")
        stime = time()
        self.__model.solve(GUROBI(msg=0, timeLimit=milp_time_limit_in_sec))
        logging.info(f"Solved within {round((time() - stime), 2)} seconds.")
        logging.info(f"Model status: {LpStatus[self.__model.status]}")
        logging.info(f"Objective value: {self.__model.objective.value()}")
        self.__extract_solution()

    def __build_decision_variables(self) -> None:
        logging.info("Building decision variables...")
        self.__build_z_variables()
        self.__build_x_variables()
        self.__build_y_variables()
        self.__build_penalty_variables()
        self.__variables = LpVariable.dicts("Variables", self.__names, cat="Binary")
        self.__add_variables = LpVariable.dicts(
            "AddVariables", self.__add_names, cat="Binary"
        )
        self.__add2_variables = LpVariable.dicts(
            "Add2Variables", self.__add2_names, cat="Binary"
        )
        self.__penalties = LpVariable.dicts(
            "Penalties", self.__pen, lowBound=0, cat="Integer"
        )

    def __build_penalty_variables(self) -> None:
        self.__build_similar_tracks_penalty_variables()
        self.__build_num_of_rooms_per_track_penalty_variables()
        self.__build_parallel_tracks_penalty_variables()

    def __build_objective_function(self) -> None:
        logging.info("Building objective function...")
        obj_function = [self.__add_variables, self.__penalties]
        all_names = [self.__add_names, self.__pen]
        self.__model += lpSum(
            [
                self.__coefficients[i] * obj_function[x][i]
                for x in range(len(obj_function))
                for i in all_names[x]
            ]
        )

    def __build_constraints(self) -> None:
        logging.info("Building constraints...")
        self.__build_assign_multi_slot_submissions_constraints()
        self.__build_assign_all_submissions_constraints()
        self.__build_assign_tracks()
        self.__build_track_chairs_conflicts_constraints()
        self.__build_similar_tracks_constraints()
        self.__build_parallel_tracks_constraints()
        self.__build_num_of_rooms_per_track_constraints()
        self.__build_assign_only_one_track_per_session_room_pair_constraints()

    def __build_z_variables(self) -> None:
        for session in range(self.__problem.get_number_of_sessions()):
            for room in range(self.__problem.get_number_of_rooms()):
                temp = []
                for track in range(self.__problem.get_number_of_tracks()):
                    self.__add_names.append(
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                    self.__timeslots[
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    ] = self.__problem.get_session(session).get_session_max_time_slots()
                    self.__coefficients[
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    ] = (
                        1
                        + self.__problem.get_parameters().tracks_sessions_penalty_weight
                        * self.__problem.get_tracks_sessions_penalty(
                            self.__problem.get_track(track).get_track_name(),
                            self.__problem.get_session(session).get_session_name(),
                        )
                        + self.__problem.get_parameters().tracks_rooms_penalty_weight
                        * self.__problem.get_tracks_rooms_penalty(
                            self.__problem.get_track(track).get_track_name(),
                            self.__problem.get_room(room).get_room_name(),
                        )
                        + self.__problem.get_parameters().sessions_rooms_penalty_weight
                        * self.__problem.get_sessions_rooms_penalty(
                            self.__problem.get_session(session).get_session_name(),
                            self.__problem.get_room(room).get_room_name(),
                        )
                    )
                    temp.append(
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                    self.__room_track_z_map[
                        self.__problem.get_room(room).get_room_name()
                        + self.__problem.get_track(track).get_track_name()
                    ].append(
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                    self.__track_z_map[
                        self.__problem.get_track(track).get_track_name()
                    ].append(
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                    self.__track_session_room_z_map[
                        self.__problem.get_track(track).get_track_name()
                        + self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_room(room).get_room_name()
                    ] = (
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                    self.__session_track_z_map[
                        self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_track(track).get_track_name()
                    ].append(
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    )
                self.__session_room_z_map[
                    self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_room(room).get_room_name()
                ] = temp

    def __build_x_variables(self) -> None:
        for session in range(self.__problem.get_number_of_sessions()):
            for room in range(self.__problem.get_number_of_rooms()):
                for multi_slot_submission in self.__mts_subs:
                    if (
                        self.__problem.get_submission(
                            multi_slot_submission
                        ).get_submission_required_time_slots()
                        <= self.__problem.get_session(
                            session
                        ).get_session_max_time_slots()
                    ):
                        self.__names.append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        )
                        self.__coefficients[
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        ] = 1
                        self.__n[
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        ] = self.__problem.get_submission(
                            multi_slot_submission
                        ).get_submission_required_time_slots()
                        self.__sub_x_map[
                            self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        ].append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        )
                        self.__track_session_room_x_map[
                            self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + self.__problem.get_session(session).get_session_name()
                            + self.__problem.get_room(room).get_room_name()
                        ].append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_submission(multi_slot_submission)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.__problem.get_submission(
                                multi_slot_submission
                            ).get_submission_name()
                        )

    def __build_y_variables(self) -> None:
        for track in range(self.__problem.get_number_of_tracks()):
            temp = []
            for room in range(self.__problem.get_number_of_rooms()):
                self.__add2_names.append(
                    "|"
                    + self.__problem.get_room(room).get_room_name()
                    + "|"
                    + self.__problem.get_track(track).get_track_name()
                )
                self.__coefficients[
                    "|"
                    + self.__problem.get_room(room).get_room_name()
                    + "|"
                    + self.__problem.get_track(track).get_track_name()
                ] = 1
                temp.append(
                    "|"
                    + self.__problem.get_room(room).get_room_name()
                    + "|"
                    + self.__problem.get_track(track).get_track_name()
                )
                self.__track_room_y_map[
                    self.__problem.get_track(track).get_track_name()
                    + self.__problem.get_room(room).get_room_name()
                ] = (
                    "|"
                    + self.__problem.get_room(room).get_room_name()
                    + "|"
                    + self.__problem.get_track(track).get_track_name()
                )
            self.__track_y_map[self.__problem.get_track(track).get_track_name()] = temp

    def __build_similar_tracks_penalty_variables(self) -> None:
        for this_track in range(self.__problem.get_number_of_tracks()):
            temp = [this_track]
            for other_track in range(this_track, self.__problem.get_number_of_tracks()):
                if this_track != other_track:
                    if (
                        self.__problem.get_tracks_tracks_penalty_by_index(
                            this_track, other_track
                        )
                        != 0
                    ):
                        temp.append(other_track)
                if len(temp) > 1:
                    for session in range(self.__problem.get_number_of_sessions()):
                        self.__pen.append(
                            "ptt_|"
                            + self.__problem.get_track(this_track).get_track_name()
                            + self.__problem.get_track(other_track).get_track_name()
                            + self.__problem.get_session(session).get_session_name()
                        )
                        self.__coefficients[
                            "ptt_|"
                            + self.__problem.get_track(this_track).get_track_name()
                            + self.__problem.get_track(other_track).get_track_name()
                            + self.__problem.get_session(session).get_session_name()
                        ] = (
                            self.__problem.get_parameters().similar_tracks_penalty_weight
                            * self.__problem.get_tracks_tracks_penalty_by_index(
                                this_track, other_track
                            )
                        )
                    temp = [this_track]

    def __build_num_of_rooms_per_track_penalty_variables(self) -> None:
        for track in range(self.__problem.get_number_of_tracks()):
            temp = []
            track_name = self.__problem.get_track(track).get_track_name()
            for name in self.__add2_names:
                if track_name == name.split("|")[2]:
                    temp.append(name)
            self.__pen.append(
                "pmrt_|" + self.__problem.get_track(track).get_track_name()
            )
            self.__coefficients[
                "pmrt_|" + self.__problem.get_track(track).get_track_name()
            ] = self.__problem.get_parameters().num_rooms_per_track_weight

    def __build_parallel_tracks_penalty_variables(self) -> None:
        for session in range(self.__problem.get_number_of_sessions()):
            session_name = self.__problem.get_session(session).get_session_name()
            for track in range(self.__problem.get_number_of_tracks()):
                track_name = self.__problem.get_track(track).get_track_name()
                temp = []
                for name in self.__add_names:
                    if (
                        session_name == name.split("|")[1]
                        and track_name == name.split("|")[3]
                    ):
                        temp.append(name)
                self.__pen.append(
                    "ppt_|"
                    + self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_track(track).get_track_name()
                )
                self.__coefficients[
                    "ppt_|"
                    + self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_track(track).get_track_name()
                ] = self.__problem.get_parameters().parallel_tracks_weight

    def __build_assign_multi_slot_submissions_constraints(self) -> None:
        constraints = []
        for track in range(self.__problem.get_number_of_tracks()):
            for session in range(self.__problem.get_number_of_sessions()):
                for room in range(self.__problem.get_number_of_rooms()):
                    temp = self.__track_session_room_x_map[
                        self.__problem.get_track(track).get_track_name()
                        + self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_room(room).get_room_name()
                    ]
                    if len(temp) != 0:
                        constraints.append(
                            lpSum([self.__n[x] * self.__variables[x] for x in temp])
                            - self.__problem.get_session(
                                session
                            ).get_session_max_time_slots()
                            * self.__add_variables[
                                self.__track_session_room_z_map[
                                    self.__problem.get_track(track).get_track_name()
                                    + self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + self.__problem.get_room(room).get_room_name()
                                ]
                            ]
                        )

        for constraint in constraints:
            self.__model += constraint <= 0

    def __build_assign_all_submissions_constraints(self) -> None:
        constraints = []
        for submission in self.__mts_subs:
            temp = self.__sub_x_map[
                self.__problem.get_submission(submission).get_submission_name()
            ]
            constraints.append(lpSum([self.__variables[x] for x in temp]))

        for constraint in constraints:
            self.__model += constraint == 1

    def __build_assign_tracks(self) -> None:
        for track in range(self.__problem.get_number_of_tracks()):
            temp = self.__track_z_map[self.__problem.get_track(track).get_track_name()]
            self.__model += (
                lpSum([self.__timeslots[x] * self.__add_variables[x] for x in temp])
                >= self.__problem.get_track(track).get_track_required_time_slots()
            )

    def __build_track_chairs_conflicts_constraints(self) -> None:
        constraints = []
        temp2 = []
        for track in range(self.__problem.get_number_of_tracks()):
            if (
                len(self.__problem.get_track(track).get_track_chair_conflicts_list())
                != 0
            ):
                for session in range(self.__problem.get_number_of_sessions()):
                    temp = []
                    for room in range(self.__problem.get_number_of_rooms()):
                        temp.append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                        )
                        for x in self.__problem.get_track(
                            track
                        ).get_track_chair_conflicts_list():
                            temp.append(
                                "|"
                                + self.__problem.get_session(session).get_session_name()
                                + "|"
                                + self.__problem.get_room(room).get_room_name()
                                + "|"
                                + x.get_track_name()
                            )
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))

        for i in range(len(temp2)):
            constraints.append(lpSum([self.__add_variables[x] for x in temp2[i]]))

        for constraint in constraints:
            self.__model += constraint <= 1

    def __build_similar_tracks_constraints(self) -> None:
        constraints = []
        for this_track in range(self.__problem.get_number_of_tracks()):
            temp = [this_track]
            for other_track in range(this_track, self.__problem.get_number_of_tracks()):
                if this_track != other_track:
                    if (
                        self.__problem.get_tracks_tracks_penalty_by_index(
                            this_track, other_track
                        )
                        != 0
                    ):
                        temp.append(other_track)
                if len(temp) > 1:
                    for session in range(self.__problem.get_number_of_sessions()):
                        session_name = self.__problem.get_session(
                            session
                        ).get_session_name()
                        temp2 = []
                        for name in range(len(self.__add_names)):
                            for z in range(len(temp)):
                                if (
                                    self.__add_names[name].split("|")[1] == session_name
                                    and self.__add_names[name].split("|")[3]
                                    == self.__problem.get_track(
                                        temp[z]
                                    ).get_track_name()
                                ):
                                    temp2.append(self.__add_names[name])
                        constraints.append(
                            lpSum([self.__add_variables[x] for x in temp2])
                            - self.__penalties[
                                "ptt_|"
                                + self.__problem.get_track(this_track).get_track_name()
                                + self.__problem.get_track(other_track).get_track_name()
                                + self.__problem.get_session(session).get_session_name()
                            ]
                            - self.__penalties[
                                "ppt_|"
                                + self.__problem.get_session(session).get_session_name()
                                + self.__problem.get_track(this_track).get_track_name()
                            ]
                            - self.__penalties[
                                "ppt_|"
                                + self.__problem.get_session(session).get_session_name()
                                + self.__problem.get_track(other_track).get_track_name()
                            ]
                        )
                    temp = [this_track]

        for constraint in constraints:
            self.__model += constraint <= 1

    def __build_parallel_tracks_constraints(self) -> None:
        constraints = []
        for session in range(self.__problem.get_number_of_sessions()):
            for track in range(self.__problem.get_number_of_tracks()):
                temp = self.__session_track_z_map[
                    self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_track(track).get_track_name()
                ]
                constraints.append(
                    lpSum([self.__add_variables[x] for x in temp])
                    - self.__penalties[
                        "ppt_|"
                        + self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_track(track).get_track_name()
                    ]
                )

        for constraint in constraints:
            self.__model += constraint <= 1

    def __build_num_of_rooms_per_track_constraints(self) -> None:
        constraints = []
        for track in range(self.__problem.get_number_of_tracks()):
            temp = self.__track_y_map[self.__problem.get_track(track).get_track_name()]
            constraints.append(
                lpSum([self.__add2_variables[x] for x in temp])
                - self.__penalties[
                    "pmrt_|" + self.__problem.get_track(track).get_track_name()
                ]
            )

        for constraint in constraints:
            self.__model += constraint == 1

        constraints = []
        for room in range(self.__problem.get_number_of_rooms()):
            for track in range(self.__problem.get_number_of_tracks()):
                temp = self.__room_track_z_map[
                    self.__problem.get_room(room).get_room_name()
                    + self.__problem.get_track(track).get_track_name()
                ]
                constraints.append(
                    lpSum([self.__add_variables[x] for x in temp])
                    - self.__problem.get_number_of_sessions()
                    * self.__add2_variables[
                        self.__track_room_y_map[
                            self.__problem.get_track(track).get_track_name()
                            + self.__problem.get_room(room).get_room_name()
                        ]
                    ]
                )

        for constraint in constraints:
            self.__model += constraint <= 0

    def __build_assign_only_one_track_per_session_room_pair_constraints(self) -> None:
        constraints = []
        for session in range(self.__problem.get_number_of_sessions()):
            for room in range(self.__problem.get_number_of_rooms()):
                temp = self.__session_room_z_map[
                    self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_room(room).get_room_name()
                ]
                constraints.append(lpSum([self.__add_variables[x] for x in temp]))

        for constraint in constraints:
            self.__model += constraint <= 1

    def __extract_solution(self) -> None:
        solution = []
        solution2 = []
        to_remove = []
        gur_vars = self.__model.solverModel.getVars()
        for i in gur_vars:
            if i.X > 0:
                solution.append(i.varName)
        for i in range(len(solution)):
            if solution[i].split("|")[0] != "AddVariables_":
                to_remove.append(solution[i])
            if solution[i].split("|")[0] == "Variables_":
                solution2.append(solution[i])
        for i in to_remove:
            if i in solution:
                solution.remove(i)

        df = pd.DataFrame(solution)
        df.replace(to_replace="_", value=" ", regex=True, inplace=True)
        df = df.map(lambda x: x.split("|"))
        solution = df.iloc[:, 0].to_list()

        if len(solution2) > 0:
            df = pd.DataFrame(solution2)
            df.replace(to_replace="_", value=" ", regex=True, inplace=True)
            df = df.map(lambda x: x.split("|"))
            solution2 = df.iloc[:, 0].to_list()

        for i in range(len(solution)):
            self.__solution.get_tracks_solution()[
                self.__problem.get_session_index(solution[i][1])
            ][
                self.__problem.get_room_index(solution[i][2])
            ] = self.__problem.get_track_index(solution[i][3])

        if len(solution2) > 0:
            for i in range(len(solution2)):
                for j in range(
                    self.__problem.get_submission(
                        self.__problem.get_submission_index(solution2[i][4])
                    ).get_submission_required_time_slots()
                ):
                    ts = self.__solution.get_submissions_solution()[
                        self.__problem.get_session_index(solution2[i][1])
                    ][self.__problem.get_room_index(solution2[i][2])].index(-1)
                    self.__solution.get_submissions_solution()[
                        self.__problem.get_session_index(solution2[i][1])
                    ][self.__problem.get_room_index(solution2[i][2])][
                        ts
                    ] = self.__problem.get_submission_index(solution2[i][4])

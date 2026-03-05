"""
Created on Thu Mar 5 11:11:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from typing import List, Dict
import pandas as pd
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, GUROBI
from solution import Solution
from time import time
import logging


class ExactModel:
    def __init__(self, problem: Problem, solution: Solution) -> None:
        self.__problem: Problem = problem
        self.__solution: Solution = solution
        self.__model: LpProblem = LpProblem("ExactModel", LpMinimize)
        self.__variables: LpVariable = None
        self.__add_variables: LpVariable = None
        self.__add2_variables: LpVariable = None
        self.__names: List[str] = list()
        self.__submissions_with_conflicts: List[int] = [
            submission
            for submission in range(self.__problem.get_number_of_submissions())
            if len(
                self.__problem.get_submission(
                    submission
                ).get_submission_presenter_conflicts_list()
            )
            != 0
        ]
        self.__submission_conflict_x_list: List[str] = list()
        self.__track_session_room_x_map: Dict[str, List[str]] = dict()
        self.__track_submission_x_map: Dict[str, List[str]] = {
            self.__problem.get_track(track).get_track_name()
            + self.__problem.get_track(track)
            .get_track_submissions_list()[sub]
            .get_submission_name(): []
            for track in range(self.__problem.get_number_of_tracks())
            for sub in range(
                len(self.__problem.get_track(track).get_track_submissions_list())
            )
        }
        self.__add_names: List[str] = list()
        self.__session_room_z_map: Dict[str, List[str]] = dict()
        self.__track_session_room_z_map: Dict[str, str] = dict()
        self.__room_track_z_map: Dict[str, List[str]] = {
            self.__problem.get_room(room).get_room_name()
            + self.__problem.get_track(track).get_track_name(): []
            for room in range(self.__problem.get_number_of_rooms())
            for track in range(self.__problem.get_number_of_tracks())
        }
        self.__add2_names: List[str] = list()
        self.__track_y_map: Dict[str, List[str]] = dict()
        self.__track_room_y_map: Dict[str, str] = dict()
        self.__coefficients: Dict[str, int] = dict()
        self.__timeslots: Dict[str, int] = dict()
        self.__required_sessions: Dict[str, int] = dict()
        self.__find_MaxS_for_tracks()
        self.__build_decision_variables()
        self.__build_objective_function()
        self.__build_constraints()

    def solve(self, time_limit_in_sec: int) -> None:
        logging.info("Solving with exact milp model...")
        stime = time()
        self.__model.solve(GUROBI(msg=0, MIPGap=0, timeLimit=time_limit_in_sec))
        logging.info(f"Solved within {round((time() - stime), 2)} seconds.")
        logging.info(f"Model status: {LpStatus[self.__model.status]}")
        logging.info(f"Objective value: {self.__model.objective.value()}")
        self.__extract_solution()

    def __build_decision_variables(self) -> None:
        logging.info("Building decision variables...")
        self.__build_x_variables()
        self.__build_y_variables()
        self.__build_z_variables()
        self.__variables = LpVariable.dicts("Variables", self.__names, cat="Binary")
        self.__add_variables = LpVariable.dicts(
            "AddVariables", self.__add_names, cat="Binary"
        )
        self.__add2_variables = LpVariable.dicts(
            "Add2Variables", self.__add2_names, cat="Binary"
        )

    def __build_objective_function(self) -> None:
        logging.info("Building objective function...")
        obj_function = [self.__variables, self.__add_variables]
        all_names = [self.__names, self.__add_names]
        self.__model += lpSum(
            [
                self.__coefficients[i] * obj_function[x][i]
                for x in range(len(obj_function))
                for i in all_names[x]
            ]
        )

    def __build_constraints(self) -> None:
        logging.info("Building constraints...")
        self.__build_presenters_conflicts_constraints()
        self.__build_assign_only_one_track_per_session_room_pair_constraints()
        self.__build_submissions_tracks_bound_constraints()
        self.__build_num_of_rooms_per_track_constraints()
        self.__build_assign_tracks_into_rooms_constraints()
        self.__build_assign_all_submissions_constraints()

    def __build_x_variables(self) -> None:
        for session in range(self.__problem.get_number_of_sessions()):
            for room in range(self.__problem.get_number_of_rooms()):
                for track in range(self.__problem.get_number_of_tracks()):
                    temp = []
                    for submission in range(
                        len(
                            self.__problem.get_track(track).get_track_submissions_list()
                        )
                    ):
                        self.__names.append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                            + "|"
                            + str(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        )
                        self.__coefficients[
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                            + "|"
                            + str(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        ] = (
                            self.__problem.get_parameters().submissions_timezones_penalty_weight
                            * self.__problem.get_submissions_timezones_penalty(
                                str(
                                    self.__problem.get_track(track)
                                    .get_track_submissions_list()[submission]
                                    .get_submission_name()
                                ),
                                self.__problem.get_session(session).get_session_name(),
                            )
                            + self.__problem.get_parameters().submissions_sessions_penalty_weight
                            * self.__problem.get_submissions_sessions_penalty(
                                str(
                                    self.__problem.get_track(track)
                                    .get_track_submissions_list()[submission]
                                    .get_submission_name()
                                ),
                                self.__problem.get_session(session).get_session_name(),
                            )
                            + self.__problem.get_parameters().submissions_rooms_penalty_weight
                            * self.__problem.get_submissions_rooms_penalty(
                                str(
                                    self.__problem.get_track(track)
                                    .get_track_submissions_list()[submission]
                                    .get_submission_name()
                                ),
                                self.__problem.get_room(room).get_room_name(),
                            )
                        )
                        self.__timeslots[
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                            + "|"
                            + str(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        ] = self.__problem.get_submission(
                            self.__problem.get_submission_index(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        ).get_submission_required_time_slots()
                        temp.append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                            + "|"
                            + str(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        )
                        self.__track_submission_x_map[
                            self.__problem.get_track(track).get_track_name()
                            + self.__problem.get_track(track)
                            .get_track_submissions_list()[submission]
                            .get_submission_name()
                        ].append(
                            "|"
                            + self.__problem.get_session(session).get_session_name()
                            + "|"
                            + self.__problem.get_room(room).get_room_name()
                            + "|"
                            + self.__problem.get_track(track).get_track_name()
                            + "|"
                            + str(
                                self.__problem.get_track(track)
                                .get_track_submissions_list()[submission]
                                .get_submission_name()
                            )
                        )
                        if (
                            len(
                                self.__problem.get_submission(
                                    self.__problem.get_submission_index(
                                        self.__problem.get_track(track)
                                        .get_track_submissions_list()[submission]
                                        .get_submission_name()
                                    )
                                ).get_submission_presenter_conflicts_list()
                            )
                            != 0
                        ):
                            self.__submission_conflict_x_list.append(
                                "|"
                                + self.__problem.get_session(session).get_session_name()
                                + "|"
                                + self.__problem.get_room(room).get_room_name()
                                + "|"
                                + self.__problem.get_track(track).get_track_name()
                                + "|"
                                + str(
                                    self.__problem.get_track(track)
                                    .get_track_submissions_list()[submission]
                                    .get_submission_name()
                                )
                            )
                    self.__track_session_room_x_map[
                        self.__problem.get_track(track).get_track_name()
                        + self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_room(room).get_room_name()
                    ] = temp

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
                    self.__coefficients[
                        "|"
                        + self.__problem.get_session(session).get_session_name()
                        + "|"
                        + self.__problem.get_room(room).get_room_name()
                        + "|"
                        + self.__problem.get_track(track).get_track_name()
                    ] = (
                        self.__problem.get_parameters().tracks_sessions_penalty_weight
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
                self.__session_room_z_map[
                    self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_room(room).get_room_name()
                ] = temp

    def __find_MaxS_for_tracks(self) -> None:
        sessions_ts = []
        for session in range(self.__problem.get_number_of_sessions()):
            sessions_ts.append(
                self.__problem.get_session(session).get_session_max_time_slots()
            )
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.__problem.get_number_of_tracks()):
            temp = []
            i = -1
            while self.__problem.get_track(track).get_track_required_time_slots() > sum(
                temp
            ):
                i += 1
                temp.append(sorted_sessions_ts[i])
                if i == self.__problem.get_number_of_sessions() - 1:
                    break
            self.__required_sessions[str(track)] = len(temp)

    def __build_presenters_conflicts_constraints(self) -> None:
        for submission in range(self.__problem.get_number_of_submissions()):
            sub_name = self.__problem.get_submission(submission).get_submission_name()
        if len(self.__submissions_with_conflicts) != 0:
            unique_conflicts = []
            for submission in range(self.__problem.get_number_of_submissions()):
                sub_name = self.__problem.get_submission(
                    submission
                ).get_submission_name()
                if (
                    len(
                        self.__problem.get_submission(
                            submission
                        ).get_submission_presenter_conflicts_list()
                    )
                    != 0
                ):
                    for conflict in self.__problem.get_submission(
                        submission
                    ).get_submission_presenter_conflicts_list():
                        for session in range(self.__problem.get_number_of_sessions()):
                            session_name = self.__problem.get_session(
                                session
                            ).get_session_name()
                            for room in range(self.__problem.get_number_of_rooms()):
                                room_name = self.__problem.get_room(
                                    room
                                ).get_room_name()
                                current_conflict = [
                                    sub_name,
                                    conflict.get_submission_name(),
                                    session_name,
                                    room_name,
                                ]
                                M_list = [
                                    len(
                                        self.__problem.get_submission(
                                            submission
                                        ).get_submission_presenter_conflicts_list()
                                    )
                                    + 1,
                                    self.__problem.get_session(
                                        session
                                    ).get_session_max_time_slots(),
                                ]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(
                                        len(self.__submission_conflict_x_list)
                                    ):
                                        if (
                                            self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[4]
                                            == sub_name
                                            and self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                            and self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            == room_name
                                        ):
                                            temp.append(
                                                self.__submission_conflict_x_list[name]
                                            )
                                        if (
                                            self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[4]
                                            == conflict.get_submission_name()
                                            and self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            != room_name
                                            and self.__submission_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                        ):
                                            temp2.append(
                                                self.__submission_conflict_x_list[name]
                                            )
                                    self.__model += (
                                        lpSum([M * self.__variables[x] for x in temp])
                                        + lpSum([self.__variables[x] for x in temp2])
                                        <= M
                                    )

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

    def __build_submissions_tracks_bound_constraints(self) -> None:
        constraints = []
        constraints2 = []
        for track in range(self.__problem.get_number_of_tracks()):
            for session in range(self.__problem.get_number_of_sessions()):
                for room in range(self.__problem.get_number_of_rooms()):
                    temp = self.__track_session_room_x_map[
                        self.__problem.get_track(track).get_track_name()
                        + self.__problem.get_session(session).get_session_name()
                        + self.__problem.get_room(room).get_room_name()
                    ]
                    constraints.append(
                        lpSum([self.__timeslots[x] * self.__variables[x] for x in temp])
                        - self.__problem.get_session(
                            session
                        ).get_session_max_time_slots()
                        * self.__add_variables[
                            self.__track_session_room_z_map[
                                self.__problem.get_track(track).get_track_name()
                                + self.__problem.get_session(session).get_session_name()
                                + self.__problem.get_room(room).get_room_name()
                            ]
                        ]
                    )
                    constraints2.append(
                        lpSum([self.__variables[x] for x in temp])
                        - self.__add_variables[
                            self.__track_session_room_z_map[
                                self.__problem.get_track(track).get_track_name()
                                + self.__problem.get_session(session).get_session_name()
                                + self.__problem.get_room(room).get_room_name()
                            ]
                        ]
                    )

        for constraint in range(len(constraints)):
            self.__model += constraints[constraint] <= 0
            self.__model += constraints2[constraint] >= 0

    def __build_num_of_rooms_per_track_constraints(self) -> None:
        constraints = []
        for track in range(self.__problem.get_number_of_tracks()):
            temp = self.__track_y_map[self.__problem.get_track(track).get_track_name()]
            constraints.append(lpSum([self.__add2_variables[x] for x in temp]))

        for constraint in constraints:
            self.__model += constraint == 1

    def __build_assign_tracks_into_rooms_constraints(self) -> None:
        constraints = []
        for room in range(self.__problem.get_number_of_rooms()):
            for track in range(self.__problem.get_number_of_tracks()):
                temp = self.__room_track_z_map[
                    self.__problem.get_room(room).get_room_name()
                    + self.__problem.get_track(track).get_track_name()
                ]
                constraints.append(
                    lpSum([self.__add_variables[x] for x in temp])
                    - self.__required_sessions[str(track)]
                    * self.__add2_variables[
                        self.__track_room_y_map[
                            self.__problem.get_track(track).get_track_name()
                            + self.__problem.get_room(room).get_room_name()
                        ]
                    ]
                )

        for constraint in constraints:
            self.__model += constraint <= 0

    def __build_assign_all_submissions_constraints(self) -> None:
        constraints = []
        for track in range(self.__problem.get_number_of_tracks()):
            for submission in range(
                len(self.__problem.get_track(track).get_track_submissions_list())
            ):
                temp = self.__track_submission_x_map[
                    self.__problem.get_track(track).get_track_name()
                    + self.__problem.get_track(track)
                    .get_track_submissions_list()[submission]
                    .get_submission_name()
                ]
                constraints.append(lpSum([self.__variables[x] for x in temp]))

        for constraint in constraints:
            self.__model += constraint == 1

    def __extract_solution(self) -> None:
        solution = []
        for i in self.__model.variables():
            if i.varValue > 0:
                solution.append(i.name)
        to_remove = []
        for i in range(len(solution)):
            if solution[i].split("|")[0] != "Variables_":
                to_remove.append(solution[i])
        for i in to_remove:
            if i in solution:
                solution.remove(i)
        df = pd.DataFrame(solution)
        df.replace(to_replace="_", value=" ", regex=True, inplace=True)
        df = df.map(lambda x: x.split("|"))
        solution = df.iloc[:, 0].to_list()
        for i in range(len(solution)):
            self.__solution.getSolTracks()[
                self.__problem.get_session_index(solution[i][1])
            ][
                self.__problem.get_room_index(solution[i][2])
            ] = self.__problem.get_track_index(solution[i][3])
            ts = self.__solution.getSolSubmissions()[
                self.__problem.get_session_index(solution[i][1])
            ][self.__problem.get_room_index(solution[i][2])].index(-1)
            self.__solution.getSolSubmissions()[
                self.__problem.get_session_index(solution[i][1])
            ][self.__problem.get_room_index(solution[i][2])][
                ts
            ] = self.__problem.get_submission_index(solution[i][4])
        for sub in range(self.__problem.get_number_of_submissions()):
            for session in range(len(self.__solution.getSolSubmissions())):
                for room in range(len(self.__solution.getSolSubmissions()[session])):
                    if sub in self.__solution.getSolSubmissions()[session][room]:
                        info = []
                        for i in range(
                            len(self.__solution.getSolSubmissions()[session][room])
                        ):
                            if (
                                self.__solution.getSolSubmissions()[session][room][i]
                                != -1
                            ):
                                if (
                                    self.__solution.getSolSubmissions()[session][room][
                                        i
                                    ]
                                    not in info
                                ):
                                    info.append(
                                        self.__solution.getSolSubmissions()[session][
                                            room
                                        ][i]
                                    )
                        temp = []
                        for i in range(len(info)):
                            while (
                                temp.count(info[i])
                                < self.__problem.get_submission(
                                    info[i]
                                ).get_submission_required_time_slots()
                            ):
                                temp.append(info[i])
                        while len(temp) < len(
                            self.__solution.getSolSubmissions()[session][room]
                        ):
                            temp.append(-1)
                        self.__solution.getSolSubmissions()[session][room] = temp

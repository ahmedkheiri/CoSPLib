"""
Created on Thu Mar 6 09:20:16 2026

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from typing import List, Dict, Literal
from pulp import (
    LpProblem,
    LpMinimize,
    LpVariable,
    lpSum,
    LpStatus,
    GUROBI,
    HiGHS,
    SCIP_PY,
)
from solution import Solution
from time import time
import pandas as pd
import logging
import config


class ExtendedModel:
    def __init__(self, problem: Problem, solution: Solution) -> None:
        self.__problem: Problem = problem
        self.__solution: Solution = solution
        self.__solver: GUROBI | HiGHS | SCIP_PY = None
        self.__model: LpProblem = LpProblem("ExtendedModel", LpMinimize)
        self.__variables: LpVariable = None
        self.__add_variables: LpVariable = None
        self.__add2_variables: LpVariable = None
        self.__product_variables: LpVariable = None
        self.__names: List[str] = []
        self.__submission_conflict_x_list: List[int] = list()
        self.__submission_att_conflict_x_list: List[int] = list()
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
        self.__similar_tracks: Dict[str, List[str]] = {
            self.__problem.get_session(session).get_session_name()
            + self.__problem.get_track(track).get_track_name(): []
            for session in range(self.__problem.get_number_of_sessions())
            for track in range(self.__problem.get_number_of_tracks())
        }
        self.__add2_names: List[str] = list()
        self.__track_y_map: Dict[str, List[str]] = dict()
        self.__track_room_y_map: Dict[str, str] = dict()
        self.__product_names: List[str] = []
        self.__coefficients: Dict[str, int] = dict()
        self.__timeslots: Dict[str, int] = dict()
        self.__required_sessions: Dict[str, int] = dict()
        self.__find_MaxS_for_tracks()
        self.__build_decision_variables()
        self.__build_objective_function()
        self.__build_constraints()
        self.__set_solver(config.SOLVER, config.TIME_LIMIT_IN_SEC, config.MIPGAP)

    def solve(self) -> None:
        logging.info("Solving with extended milp model...")
        stime = time()
        self.__model.solve(self.__solver)
        logging.info(f"Solved within {round((time() - stime), 2)} seconds.")
        logging.info(f"Model status: {LpStatus[self.__model.status]}")
        logging.info(f"Objective value: {self.__model.objective.value()}")
        self.__extract_solution()

    def __set_solver(
        self,
        solver: Literal["GUROBI", "SCIP", "HiGHS"],
        time_limit_in_sec: int,
        MIPGap: float,
    ) -> None:
        if solver == "GUROBI":
            self.__solver = GUROBI(MIPGap=MIPGap, timeLimit=time_limit_in_sec, IntegralityFocus=1)
            return
        if solver == "SCIP":
            self.__solver = SCIP_PY(gapRel=MIPGap, timeLimit=time_limit_in_sec)
            return
        if solver == "HiGHS":
            self.__solver = HiGHS(gapRel=MIPGap, timeLimit=time_limit_in_sec)
            return
        raise ValueError(
            f"{config.SOLVER} is not supported!\nSupported solvers: 'GUROBI', 'SCIP', 'HiGHS'"
        )

    def __build_decision_variables(self) -> None:
        logging.info("Building decision variables...")
        self.__build_x_variables()
        self.__build_y_variables()
        self.__build_z_variables()
        self.__build_product_variables()
        self.__variables = LpVariable.dicts("Variables", self.__names, cat="Binary")
        self.__add_variables = LpVariable.dicts(
            "AddVariables", self.__add_names, cat="Binary"
        )
        self.__add2_variables = LpVariable.dicts(
            "Add2Variables", self.__add2_names, cat="Binary"
        )
        self.__product_variables = LpVariable.dicts(
            "ProdVariables", self.__product_names, cat="Binary"
        )

    def __build_objective_function(self) -> None:
        logging.info("Building objective function...")
        obj_function = [
            self.__variables,
            self.__add_variables,
            self.__product_variables,
        ]
        all_names = [self.__names, self.__add_names, self.__product_names]
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
        self.__build_similar_tracks_constraints()
        self.__build_track_chairs_conflicts_constraints()
        self.__build_attendees_conflicts_constraints()
        self.__build_product_variables_constraints()

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
                        if (
                            len(
                                self.__problem.get_submission(
                                    self.__problem.get_submission_index(
                                        self.__problem.get_track(track)
                                        .get_track_submissions_list()[submission]
                                        .get_submission_name()
                                    )
                                ).get_submission_attendee_conflicts_list()
                            )
                            != 0
                        ):
                            self.__submission_att_conflict_x_list.append(
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
                    for other_track in range(
                        track + 1, self.__problem.get_number_of_tracks()
                    ):
                        if (
                            self.__problem.get_tracks_tracks_penalty_by_index(
                                track, other_track
                            )
                            != 0
                        ):
                            if (
                                "|"
                                + self.__problem.get_session(session).get_session_name()
                                + "|"
                                + self.__problem.get_room(room).get_room_name()
                                + "|"
                                + self.__problem.get_track(track).get_track_name()
                                not in self.__similar_tracks[
                                    self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + self.__problem.get_track(track).get_track_name()
                                ]
                            ):
                                self.__similar_tracks[
                                    self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + self.__problem.get_track(track).get_track_name()
                                ].append(
                                    "|"
                                    + self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + "|"
                                    + self.__problem.get_room(room).get_room_name()
                                    + "|"
                                    + self.__problem.get_track(track).get_track_name()
                                )
                            if (
                                "|"
                                + self.__problem.get_session(session).get_session_name()
                                + "|"
                                + self.__problem.get_room(room).get_room_name()
                                + "|"
                                + self.__problem.get_track(other_track).get_track_name()
                                not in self.__similar_tracks[
                                    self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + self.__problem.get_track(track).get_track_name()
                                ]
                            ):
                                self.__similar_tracks[
                                    self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + self.__problem.get_track(track).get_track_name()
                                ].append(
                                    "|"
                                    + self.__problem.get_session(
                                        session
                                    ).get_session_name()
                                    + "|"
                                    + self.__problem.get_room(room).get_room_name()
                                    + "|"
                                    + self.__problem.get_track(
                                        other_track
                                    ).get_track_name()
                                )
                self.__session_room_z_map[
                    self.__problem.get_session(session).get_session_name()
                    + self.__problem.get_room(room).get_room_name()
                ] = temp

    def __build_product_variables(self) -> None:
        for i in range(
            self.__problem.get_number_of_rooms() * self.__problem.get_number_of_tracks()
        ):
            temp = []
            temp.append(self.__add_names[i])
            for j in range(len(self.__add_names)):
                if (
                    self.__add_names[i].split("|")[1]
                    != self.__add_names[j].split("|")[1]
                    and self.__add_names[i].split("|")[2]
                    == self.__add_names[j].split("|")[2]
                    and self.__add_names[i].split("|")[3]
                    == self.__add_names[j].split("|")[3]
                ):
                    temp.append(self.__add_names[j])
            for z in range(len(temp) - 1):
                temp2 = temp[z] + temp[z + 1]
                self.__product_names.append(temp2)
                self.__coefficients[
                    temp2
                ] = -self.__problem.get_parameters().consecutive_tracks_weight

    def __build_presenters_conflicts_constraints(self) -> None:
        if len(self.__submission_conflict_x_list) != 0:
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

        for c in range(len(constraints)):
            self.__model += constraints[c] <= 0
            self.__model += constraints2[c] >= 0

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

    def __build_similar_tracks_constraints(self) -> None:
        constraints = []
        for i in self.__similar_tracks.values():
            if len(i) != 0:
                temp = i
                constraints.append(lpSum([self.__add_variables[x] for x in temp]))

        for constraint in constraints:
            self.__model += constraint <= 1

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

    def __build_attendees_conflicts_constraints(self) -> None:
        if len(self.__submission_att_conflict_x_list) != 0:
            unique_conflicts = []
            for submission in range(self.__problem.get_number_of_submissions()):
                sub_name = self.__problem.get_submission(
                    submission
                ).get_submission_name()
                if (
                    len(
                        self.__problem.get_submission(
                            submission
                        ).get_submission_attendee_conflicts_list()
                    )
                    != 0
                ):
                    for conflict in self.__problem.get_submission(
                        submission
                    ).get_submission_attendee_conflicts_list():
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
                                        ).get_submission_attendee_conflicts_list()
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
                                        len(self.__submission_att_conflict_x_list)
                                    ):
                                        if (
                                            self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[4]
                                            == sub_name
                                            and self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                            and self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            == room_name
                                        ):
                                            temp.append(
                                                self.__submission_att_conflict_x_list[
                                                    name
                                                ]
                                            )
                                        if (
                                            self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[4]
                                            == conflict.get_submission_name()
                                            and self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            != room_name
                                            and self.__submission_att_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                        ):
                                            temp2.append(
                                                self.__submission_att_conflict_x_list[
                                                    name
                                                ]
                                            )
                                    self.__model += (
                                        lpSum([M * self.__variables[x] for x in temp])
                                        + lpSum([self.__variables[x] for x in temp2])
                                        <= M
                                    )

    def __build_product_variables_constraints(self) -> None:
        constraints = []
        constraints2 = []
        for i in range(
            self.__problem.get_number_of_rooms() * self.__problem.get_number_of_tracks()
        ):
            temp = []
            temp.append(self.__add_names[i])
            for j in range(len(self.__add_names)):
                if (
                    self.__add_names[i].split("|")[1]
                    != self.__add_names[j].split("|")[1]
                    and self.__add_names[i].split("|")[2]
                    == self.__add_names[j].split("|")[2]
                    and self.__add_names[i].split("|")[3]
                    == self.__add_names[j].split("|")[3]
                ):
                    temp.append(self.__add_names[j])
            for z in range(len(temp) - 1):
                temp2 = temp[z] + temp[z + 1]
                constraints.append(
                    self.__product_variables[temp2]
                    - self.__add_variables[temp[z]]
                    - self.__add_variables[temp[z + 1]]
                )
                constraints2.append(
                    self.__product_variables[temp2] - self.__add_variables[temp[z]]
                )
                constraints2.append(
                    self.__product_variables[temp2] - self.__add_variables[temp[z + 1]]
                )

        for constraint in constraints:
            self.__model += constraint >= -1

        for constraint in constraints2:
            self.__model += constraint <= 0

    def __convert_float_to_int(self, float_value: float) -> int:
        return int(round(float_value, ndigits=6))

    def __extract_solution(self) -> None:
        solution = []
        for i in self.__model.variables():
            if self.__convert_float_to_int(i.varValue) > 0:
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
            self.__solution.get_tracks_solution()[
                self.__problem.get_session_index(solution[i][1])
            ][
                self.__problem.get_room_index(solution[i][2])
            ] = self.__problem.get_track_index(solution[i][3])
            ts = self.__solution.get_submissions_solution()[
                self.__problem.get_session_index(solution[i][1])
            ][self.__problem.get_room_index(solution[i][2])].index(-1)
            self.__solution.get_submissions_solution()[
                self.__problem.get_session_index(solution[i][1])
            ][self.__problem.get_room_index(solution[i][2])][
                ts
            ] = self.__problem.get_submission_index(solution[i][4])
        for sub in range(self.__problem.get_number_of_submissions()):
            for session in range(len(self.__solution.get_submissions_solution())):
                for room in range(
                    len(self.__solution.get_submissions_solution()[session])
                ):
                    if sub in self.__solution.get_submissions_solution()[session][room]:
                        info = []
                        for i in range(
                            len(
                                self.__solution.get_submissions_solution()[session][
                                    room
                                ]
                            )
                        ):
                            if (
                                self.__solution.get_submissions_solution()[session][
                                    room
                                ][i]
                                != -1
                            ):
                                if (
                                    self.__solution.get_submissions_solution()[session][
                                        room
                                    ][i]
                                    not in info
                                ):
                                    info.append(
                                        self.__solution.get_submissions_solution()[
                                            session
                                        ][room][i]
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
                            self.__solution.get_submissions_solution()[session][room]
                        ):
                            temp.append(-1)
                        self.__solution.get_submissions_solution()[session][room] = temp

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

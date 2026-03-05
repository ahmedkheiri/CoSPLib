# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from solution import Solution
from pulp import LpProblem, LpMinimize, LpVariable, lpSum, LpStatus, GUROBI
import pandas as pd
import numpy as np
from time import time


class Optimisation:
    def __init__(self, problem: Problem, solution: Solution):
        self.__problem = problem
        self.__solution = solution

    def get_problem(self) -> Problem:
        return self.__problem

    def get_solution(self) -> Solution:
        return self.__solution

    def TracksExactModel(self, timelimit):
        model = LpProblem("model", LpMinimize)
        names = []
        sub_x_map = {
            self.get_problem().get_submission(sub).get_submission_name(): []
            for sub in range(self.get_problem().get_number_of_submissions())
            if self.get_problem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            > 1
        }
        track_session_room_x_map = {
            self.get_problem().get_track(track).get_track_name()
            + self.get_problem().get_session(session).get_session_name()
            + self.get_problem().get_room(room).get_room_name(): []
            for track in range(self.get_problem().get_number_of_tracks())
            for session in range(self.get_problem().get_number_of_sessions())
            for room in range(self.get_problem().get_number_of_rooms())
        }
        add_names = []
        track_z_map = {
            self.get_problem().get_track(track).get_track_name(): []
            for track in range(self.get_problem().get_number_of_tracks())
        }
        session_room_z_map = {}
        room_track_z_map = {
            self.get_problem().get_room(room).get_room_name()
            + self.get_problem().get_track(track).get_track_name(): []
            for room in range(self.get_problem().get_number_of_rooms())
            for track in range(self.get_problem().get_number_of_tracks())
        }
        track_session_room_z_map = {}
        session_track_z_map = {
            self.get_problem().get_session(session).get_session_name()
            + self.get_problem().get_track(track).get_track_name(): []
            for session in range(self.get_problem().get_number_of_sessions())
            for track in range(self.get_problem().get_number_of_tracks())
        }
        add2_names = []
        track_room_y_map = {}
        track_y_map = {}
        product_names = []
        coefficients = {}
        timeslots = {}
        n = {}
        mts_subs = [
            sub
            for sub in range(self.get_problem().get_number_of_submissions())
            if self.get_problem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            > 1
        ]

        # Creating decision variables Zs
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                temp = []
                for z in range(self.get_problem().get_number_of_tracks()):
                    add_names.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    timeslots[
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    ] = self.get_problem().get_session(i).get_session_max_time_slots()
                    coefficients[
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    ] = (
                        1
                        + self.get_problem()
                        .get_parameters()
                        .tracks_sessions_penalty_weight
                        * self.get_problem().get_tracks_sessions_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_session(i).get_session_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .tracks_rooms_penalty_weight
                        * self.get_problem().get_tracks_rooms_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .sessions_rooms_penalty_weight
                        * self.get_problem().get_sessions_rooms_penalty(
                            self.get_problem().get_session(i).get_session_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                    )
                    temp.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    room_track_z_map[
                        self.get_problem().get_room(j).get_room_name()
                        + self.get_problem().get_track(z).get_track_name()
                    ].append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    track_z_map[
                        self.get_problem().get_track(z).get_track_name()
                    ].append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    track_session_room_z_map[
                        self.get_problem().get_track(z).get_track_name()
                        + self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_room(j).get_room_name()
                    ] = (
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    session_track_z_map[
                        self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_track(z).get_track_name()
                    ].append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                session_room_z_map[
                    self.get_problem().get_session(i).get_session_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = temp

        # Creating decision variables Xs
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                for x in mts_subs:
                    if (
                        self.get_problem()
                        .get_submission(x)
                        .get_submission_required_time_slots()
                        <= self.get_problem()
                        .get_session(i)
                        .get_session_max_time_slots()
                    ):
                        names.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.get_problem().get_submission(x).get_submission_name()
                        )
                        coefficients[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.get_problem().get_submission(x).get_submission_name()
                        ] = 1
                        n[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.get_problem().get_submission(x).get_submission_name()
                        ] = (
                            self.get_problem()
                            .get_submission(x)
                            .get_submission_required_time_slots()
                        )
                        sub_x_map[
                            self.get_problem().get_submission(x).get_submission_name()
                        ].append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.get_problem().get_submission(x).get_submission_name()
                        )
                        track_session_room_x_map[
                            self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + self.get_problem().get_session(i).get_session_name()
                            + self.get_problem().get_room(j).get_room_name()
                        ].append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem()
                            .get_submission(x)
                            .get_submission_track()
                            .get_track_name()
                            + "|"
                            + self.get_problem().get_submission(x).get_submission_name()
                        )

        # Additional variables to minimise tracks per room Ys
        for i in range(self.get_problem().get_number_of_tracks()):
            temp = []
            for j in range(self.get_problem().get_number_of_rooms()):
                add2_names.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                coefficients[
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                ] = 1
                temp.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                track_room_y_map[
                    self.get_problem().get_track(i).get_track_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = (
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
            track_y_map[self.get_problem().get_track(i).get_track_name()] = temp

        pen = []
        # Creating penalties for similar tracks
        for i in range(self.get_problem().get_number_of_tracks()):
            temp = [i]
            for j in range(i, self.get_problem().get_number_of_tracks()):
                if i != j:
                    if self.get_problem().get_tracks_tracks_penalty_by_index(i, j) != 0:
                        temp.append(j)
                if len(temp) > 1:
                    for session in range(self.get_problem().get_number_of_sessions()):
                        pen.append(
                            "ptt_|"
                            + self.get_problem().get_track(i).get_track_name()
                            + self.get_problem().get_track(j).get_track_name()
                            + self.get_problem().get_session(session).get_session_name()
                        )
                        coefficients[
                            "ptt_|"
                            + self.get_problem().get_track(i).get_track_name()
                            + self.get_problem().get_track(j).get_track_name()
                            + self.get_problem().get_session(session).get_session_name()
                        ] = (
                            self.get_problem()
                            .get_parameters()
                            .similar_tracks_penalty_weight
                            * self.get_problem().get_tracks_tracks_penalty_by_index(
                                i, j
                            )
                        )
                    temp = [i]

        # Creating penalties for min number of rooms per track
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = []
            track_name = self.get_problem().get_track(track).get_track_name()
            for name in add2_names:
                if track_name == name.split("|")[2]:
                    temp.append(name)
            pen.append("pmrt_|" + self.get_problem().get_track(track).get_track_name())
            coefficients[
                "pmrt_|" + self.get_problem().get_track(track).get_track_name()
            ] = self.get_problem().get_parameters().num_rooms_per_track_weight

        # Creating penalties for parallel tracks
        for session in range(self.get_problem().get_number_of_sessions()):
            session_name = self.get_problem().get_session(session).get_session_name()
            for track in range(self.get_problem().get_number_of_tracks()):
                track_name = self.get_problem().get_track(track).get_track_name()
                temp = []
                for name in add_names:
                    if (
                        session_name == name.split("|")[1]
                        and track_name == name.split("|")[3]
                    ):
                        temp.append(name)
                pen.append(
                    "ppt_|"
                    + self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_track(track).get_track_name()
                )
                coefficients[
                    "ppt_|"
                    + self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_track(track).get_track_name()
                ] = self.get_problem().get_parameters().parallel_tracks_weight

        # Creating objective function and binary IP formulation
        variables = LpVariable.dicts("Variables", names, cat="Binary")
        add_variables = LpVariable.dicts("AddVariables", add_names, cat="Binary")
        add2_variables = LpVariable.dicts("Add2Variables", add2_names, cat="Binary")
        product_variables = LpVariable.dicts(
            "ProdVariables", product_names, cat="Binary"
        )
        penalties = LpVariable.dicts("Penalties", pen, lowBound=0, cat="Integer")
        obj_function = [add_variables, penalties]
        all_names = [add_names, pen]
        model += lpSum(
            [
                coefficients[i] * obj_function[x][i]
                for x in range(len(obj_function))
                for i in all_names[x]
            ]
        )

        # Assign subs with multiple ts
        all_constraints = []
        for track in range(self.get_problem().get_number_of_tracks()):
            for session in range(self.get_problem().get_number_of_sessions()):
                for room in range(self.get_problem().get_number_of_rooms()):
                    temp = track_session_room_x_map[
                        self.get_problem().get_track(track).get_track_name()
                        + self.get_problem().get_session(session).get_session_name()
                        + self.get_problem().get_room(room).get_room_name()
                    ]
                    if len(temp) != 0:
                        all_constraints.append(
                            lpSum([n[x] * variables[x] for x in temp])
                            - self.get_problem()
                            .get_session(session)
                            .get_session_max_time_slots()
                            * add_variables[
                                track_session_room_z_map[
                                    self.get_problem().get_track(track).get_track_name()
                                    + self.get_problem()
                                    .get_session(session)
                                    .get_session_name()
                                    + self.get_problem().get_room(room).get_room_name()
                                ]
                            ]
                        )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0

        # Creating Constraints: All submissions must be scheduled
        all_constraints = []
        for submission in mts_subs:
            temp = sub_x_map[
                self.get_problem().get_submission(submission).get_submission_name()
            ]
            all_constraints.append(lpSum([variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        # Creating constraints: Assign tracks with respect to available time slots
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = track_z_map[self.get_problem().get_track(track).get_track_name()]
            model += (
                lpSum([timeslots[x] * add_variables[x] for x in temp])
                >= self.get_problem().get_track(track).get_track_required_time_slots()
            )

        # Creating constraints: Consider organiser conflicts
        all_constraints = []
        temp2 = []
        for z in range(self.get_problem().get_number_of_tracks()):
            if len(self.get_problem().get_track(z).get_trackChairConflictsList()) != 0:
                for i in range(self.get_problem().get_number_of_sessions()):
                    temp = []
                    for j in range(self.get_problem().get_number_of_rooms()):
                        temp.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                        )
                        for x in (
                            self.get_problem()
                            .get_track(z)
                            .get_trackChairConflictsList()
                        ):
                            temp.append(
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + x.get_track_name()
                            )
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints for similar tracks
        all_constraints = []
        for i in range(self.get_problem().get_number_of_tracks()):
            temp = [i]
            for j in range(i, self.get_problem().get_number_of_tracks()):
                if i != j:
                    if self.get_problem().get_tracks_tracks_penalty_by_index(i, j) != 0:
                        temp.append(j)
                if len(temp) > 1:
                    for session in range(self.get_problem().get_number_of_sessions()):
                        session_name = (
                            self.get_problem().get_session(session).get_session_name()
                        )
                        temp2 = []
                        for name in range(len(add_names)):
                            for z in range(len(temp)):
                                if (
                                    add_names[name].split("|")[1] == session_name
                                    and add_names[name].split("|")[3]
                                    == self.get_problem()
                                    .get_track(temp[z])
                                    .get_track_name()
                                ):
                                    temp2.append(add_names[name])
                        all_constraints.append(
                            lpSum([add_variables[x] for x in temp2])
                            - penalties[
                                "ptt_|"
                                + self.get_problem().get_track(i).get_track_name()
                                + self.get_problem().get_track(j).get_track_name()
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                            ]
                            - penalties[
                                "ppt_|"
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_track(i).get_track_name()
                            ]
                            - penalties[
                                "ppt_|"
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_track(j).get_track_name()
                            ]
                        )
                    temp = [i]

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints: Do not assign same track into same session
        all_constraints = []
        for session in range(self.get_problem().get_number_of_sessions()):
            for track in range(self.get_problem().get_number_of_tracks()):
                temp = session_track_z_map[
                    self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_track(track).get_track_name()
                ]
                all_constraints.append(
                    lpSum([add_variables[x] for x in temp])
                    - penalties[
                        "ppt_|"
                        + self.get_problem().get_session(session).get_session_name()
                        + self.get_problem().get_track(track).get_track_name()
                    ]
                )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints: Min number of Rooms per Track
        all_constraints = []
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = track_y_map[self.get_problem().get_track(track).get_track_name()]
            all_constraints.append(
                lpSum([add2_variables[x] for x in temp])
                - penalties[
                    "pmrt_|" + self.get_problem().get_track(track).get_track_name()
                ]
            )

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        all_constraints = []
        for room in range(self.get_problem().get_number_of_rooms()):
            for track in range(self.get_problem().get_number_of_tracks()):
                temp = room_track_z_map[
                    self.get_problem().get_room(room).get_room_name()
                    + self.get_problem().get_track(track).get_track_name()
                ]
                all_constraints.append(
                    lpSum([add_variables[x] for x in temp])
                    - self.get_problem().get_number_of_sessions()
                    * add2_variables[
                        track_room_y_map[
                            self.get_problem().get_track(track).get_track_name()
                            + self.get_problem().get_room(room).get_room_name()
                        ]
                    ]
                )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0

        # Creating constraints: Assign only 1 track into one room and session
        all_constraints = []
        for session in range(self.get_problem().get_number_of_sessions()):
            for room in range(self.get_problem().get_number_of_rooms()):
                temp = session_room_z_map[
                    self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_room(room).get_room_name()
                ]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Solving
        print("-------- Solving mathematical model --------")
        stime = time()
        model.solve(
            GUROBI(msg=0, timeLimit=timelimit)
        )  # StartNodeLimit / TuneTimeLimit / timeLimit / threads
        print("-------- Mathematical model solved --------")
        t = round(time() - stime, 2)
        print("Solving time:", round((time() - stime), 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])

        solution = []
        solution2 = []
        to_remove = []
        gur_vars = model.solverModel.getVars()
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
            self.get_solution().getSolTracks()[
                self.get_problem().get_session_index(solution[i][1])
            ][
                self.get_problem().get_room_index(solution[i][2])
            ] = self.get_problem().get_track_index(solution[i][3])

        if len(solution2) > 0:
            for i in range(len(solution2)):
                for j in range(
                    self.get_problem()
                    .get_submission(
                        self.get_problem().get_submission_index(solution2[i][4])
                    )
                    .get_submission_required_time_slots()
                ):
                    ts = (
                        self.get_solution()
                        .getSolSubmissions()[
                            self.get_problem().get_session_index(solution2[i][1])
                        ][self.get_problem().get_room_index(solution2[i][2])]
                        .index(-1)
                    )
                    self.get_solution().getSolSubmissions()[
                        self.get_problem().get_session_index(solution2[i][1])
                    ][self.get_problem().get_room_index(solution2[i][2])][
                        ts
                    ] = self.get_problem().get_submission_index(solution2[i][4])
        return t

    def SwapTrack(self):
        if self.get_problem().get_number_of_tracks() == 1:
            return
        session = np.random.randint(self.get_problem().get_number_of_sessions(), size=2)
        room = np.random.randint(self.get_problem().get_number_of_rooms(), size=2)
        while (
            (session[0] == session[1] and room[0] == room[1])
            or (
                self.get_solution().getSolTracks()[session[0]][room[0]]
                + self.get_solution().getSolTracks()[session[1]][room[1]]
                == -2
            )
            or (
                self.get_solution().getSolTracks()[session[0]][room[0]]
                == self.get_solution().getSolTracks()[session[1]][room[1]]
            )
        ):
            session = np.random.randint(
                self.get_problem().get_number_of_sessions(), size=2
            )
            room = np.random.randint(self.get_problem().get_number_of_rooms(), size=2)
        (
            self.get_solution().getSolTracks()[session[0]][room[0]],
            self.get_solution().getSolTracks()[session[1]][room[1]],
        ) = (
            self.get_solution().getSolTracks()[session[1]][room[1]],
            self.get_solution().getSolTracks()[session[0]][room[0]],
        )

    def SwapSubmission(self):
        track = np.random.randint(self.get_problem().get_number_of_tracks())
        subs = np.random.randint(
            len(self.get_solution().getIndSolSubmissions()[track]), size=2
        )
        while (subs[0] == subs[1]) or (
            len(self.get_solution().getIndSolSubmissions()[track]) == 1
        ):
            track = np.random.randint(self.get_problem().get_number_of_tracks())
            subs = np.random.randint(
                len(self.get_solution().getIndSolSubmissions()[track]), size=2
            )
        (
            self.get_solution().getIndSolSubmissions()[track][subs[0]],
            self.get_solution().getIndSolSubmissions()[track][subs[1]],
        ) = (
            self.get_solution().getIndSolSubmissions()[track][subs[1]],
            self.get_solution().getIndSolSubmissions()[track][subs[0]],
        )

    def ReverseSubmission(self):
        track = np.random.randint(self.get_problem().get_number_of_tracks())
        locs = np.random.randint(
            len(self.get_solution().getIndSolSubmissions()[track]), size=2
        )
        while (locs[0] == locs[1]) or (
            len(self.get_solution().getIndSolSubmissions()[track]) == 1
        ):
            track = np.random.randint(self.get_problem().get_number_of_tracks())
            locs = np.random.randint(
                len(self.get_solution().getIndSolSubmissions()[track]), size=2
            )
        loc = sorted(locs)
        temp = self.get_solution().getIndSolSubmissions()[track][loc[0] : loc[1]]
        temp.reverse()
        self.get_solution().getIndSolSubmissions()[track][loc[0] : loc[1]] = temp


class ExactModel(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)

    def solve(self, timelimit=3600):
        t_b = time()
        model = LpProblem("model", LpMinimize)
        names = []
        subs_with_conflicts = [
            sub
            for sub in range(self.get_problem().get_number_of_submissions())
            if len(
                self.get_problem()
                .get_submission(sub)
                .get_submission_presenter_conflicts_list()
            )
            != 0
        ]
        submission_conflict_x_list = []
        track_session_room_x_map = {}
        track_submission_x_map = {
            self.get_problem().get_track(track).get_track_name()
            + self.get_problem()
            .get_track(track)
            .get_track_submissions_list()[sub]
            .get_submission_name(): []
            for track in range(self.get_problem().get_number_of_tracks())
            for sub in range(
                len(self.get_problem().get_track(track).get_track_submissions_list())
            )
        }
        add_names = []
        session_room_z_map = {}
        track_session_room_z_map = {}
        room_track_z_map = {
            self.get_problem().get_room(room).get_room_name()
            + self.get_problem().get_track(track).get_track_name(): []
            for room in range(self.get_problem().get_number_of_rooms())
            for track in range(self.get_problem().get_number_of_tracks())
        }
        add2_names = []
        track_y_map = {}
        track_room_y_map = {}
        coefficients = {}
        timeslots = {}

        # Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.get_problem().get_number_of_sessions()):
            sessions_ts.append(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = []
            i = -1
            while self.get_problem().get_track(
                track
            ).get_track_required_time_slots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
                if i == self.get_problem().get_number_of_sessions() - 1:
                    break
            required_sessions[str(track)] = len(temp)

        # Creating decision variables [X Variables]
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                for z in range(self.get_problem().get_number_of_tracks()):
                    temp = []
                    for x in range(
                        len(
                            self.get_problem().get_track(z).get_track_submissions_list()
                        )
                    ):
                        names.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        coefficients[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        ] = (
                            self.get_problem()
                            .get_parameters()
                            .submissions_timezones_penalty_weight
                            * self.get_problem().get_submissions_timezones_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_session(i).get_session_name(),
                            )
                            + self.get_problem()
                            .get_parameters()
                            .submissions_sessions_penalty_weight
                            * self.get_problem().get_submissions_sessions_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_session(i).get_session_name(),
                            )
                            + self.get_problem()
                            .get_parameters()
                            .submissions_rooms_penalty_weight
                            * self.get_problem().get_submissions_rooms_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_room(j).get_room_name(),
                            )
                        )
                        timeslots[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        ] = (
                            self.get_problem()
                            .get_submission(
                                self.get_problem().get_submission_index(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                )
                            )
                            .get_submission_required_time_slots()
                        )
                        temp.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        track_submission_x_map[
                            self.get_problem().get_track(z).get_track_name()
                            + self.get_problem()
                            .get_track(z)
                            .get_track_submissions_list()[x]
                            .get_submission_name()
                        ].append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        if (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_problem().get_submission_index(
                                        self.get_problem()
                                        .get_track(z)
                                        .get_track_submissions_list()[x]
                                        .get_submission_name()
                                    )
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        ):
                            submission_conflict_x_list.append(
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + self.get_problem().get_track(z).get_track_name()
                                + "|"
                                + str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                )
                            )
                    track_session_room_x_map[
                        self.get_problem().get_track(z).get_track_name()
                        + self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_room(j).get_room_name()
                    ] = temp

        # Additional variables to minimise tracks per room [Y Variables]
        for i in range(self.get_problem().get_number_of_tracks()):
            temp = []
            for j in range(self.get_problem().get_number_of_rooms()):
                add2_names.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                temp.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                track_room_y_map[
                    self.get_problem().get_track(i).get_track_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = (
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
            track_y_map[self.get_problem().get_track(i).get_track_name()] = temp

        # Additional variables for assigning tracks into sessions and rooms [Z Variables]
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                temp = []
                for z in range(self.get_problem().get_number_of_tracks()):
                    add_names.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    coefficients[
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    ] = (
                        self.get_problem()
                        .get_parameters()
                        .tracks_sessions_penalty_weight
                        * self.get_problem().get_tracks_sessions_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_session(i).get_session_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .tracks_rooms_penalty_weight
                        * self.get_problem().get_tracks_rooms_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .sessions_rooms_penalty_weight
                        * self.get_problem().get_sessions_rooms_penalty(
                            self.get_problem().get_session(i).get_session_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                    )
                    temp.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    track_session_room_z_map[
                        self.get_problem().get_track(z).get_track_name()
                        + self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_room(j).get_room_name()
                    ] = (
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    room_track_z_map[
                        self.get_problem().get_room(j).get_room_name()
                        + self.get_problem().get_track(z).get_track_name()
                    ].append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                session_room_z_map[
                    self.get_problem().get_session(i).get_session_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = temp

        # Creating objective function and binary IP formulation
        variables = LpVariable.dicts("Variables", names, cat="Binary")
        add_variables = LpVariable.dicts("AddVariables", add_names, cat="Binary")
        add2_variables = LpVariable.dicts("Add2Variables", add2_names, cat="Binary")
        obj_function = [variables, add_variables]
        all_names = [names, add_names]
        model += lpSum(
            [
                coefficients[i] * obj_function[x][i]
                for x in range(len(obj_function))
                for i in all_names[x]
            ]
        )

        # Creating Constraints Eq.2
        if len(subs_with_conflicts) != 0:
            unique_conflicts = []
            for submission in range(self.get_problem().get_number_of_submissions()):
                sub_name = (
                    self.get_problem().get_submission(submission).get_submission_name()
                )
                if (
                    len(
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_presenter_conflicts_list()
                    )
                    != 0
                ):
                    for conflict in (
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_presenter_conflicts_list()
                    ):
                        for session in range(
                            self.get_problem().get_number_of_sessions()
                        ):
                            session_name = (
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                            )
                            for room in range(self.get_problem().get_number_of_rooms()):
                                room_name = (
                                    self.get_problem().get_room(room).get_room_name()
                                )
                                current_conflict = [
                                    sub_name,
                                    conflict.get_submission_name(),
                                    session_name,
                                    room_name,
                                ]
                                M_list = [
                                    len(
                                        self.get_problem()
                                        .get_submission(submission)
                                        .get_submission_presenter_conflicts_list()
                                    )
                                    + 1,
                                    self.get_problem()
                                    .get_session(session)
                                    .get_session_max_time_slots(),
                                ]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(len(submission_conflict_x_list)):
                                        if (
                                            submission_conflict_x_list[name].split("|")[
                                                4
                                            ]
                                            == sub_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[1]
                                            == session_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[2]
                                            == room_name
                                        ):
                                            temp.append(
                                                submission_conflict_x_list[name]
                                            )
                                        if (
                                            submission_conflict_x_list[name].split("|")[
                                                4
                                            ]
                                            == conflict.get_submission_name()
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[2]
                                            != room_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[1]
                                            == session_name
                                        ):
                                            temp2.append(
                                                submission_conflict_x_list[name]
                                            )
                                    model += (
                                        lpSum([M * variables[x] for x in temp])
                                        + lpSum([variables[x] for x in temp2])
                                        <= M
                                    )

        # Creating constraints Eq.5
        all_constraints = []
        for session in range(self.get_problem().get_number_of_sessions()):
            for room in range(self.get_problem().get_number_of_rooms()):
                temp = session_room_z_map[
                    self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_room(room).get_room_name()
                ]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints Eq.6 & Eq.7
        all_constraints = []
        all_constraints2 = []
        for track in range(self.get_problem().get_number_of_tracks()):
            for session in range(self.get_problem().get_number_of_sessions()):
                for room in range(self.get_problem().get_number_of_rooms()):
                    temp = track_session_room_x_map[
                        self.get_problem().get_track(track).get_track_name()
                        + self.get_problem().get_session(session).get_session_name()
                        + self.get_problem().get_room(room).get_room_name()
                    ]
                    all_constraints.append(
                        lpSum([timeslots[x] * variables[x] for x in temp])
                        - self.get_problem()
                        .get_session(session)
                        .get_session_max_time_slots()
                        * add_variables[
                            track_session_room_z_map[
                                self.get_problem().get_track(track).get_track_name()
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_room(room).get_room_name()
                            ]
                        ]
                    )
                    all_constraints2.append(
                        lpSum([variables[x] for x in temp])
                        - add_variables[
                            track_session_room_z_map[
                                self.get_problem().get_track(track).get_track_name()
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_room(room).get_room_name()
                            ]
                        ]
                    )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
            model += all_constraints2[c] >= 0

        # Creating constraints Eq.3
        all_constraints = []
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = track_y_map[self.get_problem().get_track(track).get_track_name()]
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        # Creating constraints Eq.4
        all_constraints = []
        for room in range(self.get_problem().get_number_of_rooms()):
            for track in range(self.get_problem().get_number_of_tracks()):
                temp = room_track_z_map[
                    self.get_problem().get_room(room).get_room_name()
                    + self.get_problem().get_track(track).get_track_name()
                ]
                all_constraints.append(
                    lpSum([add_variables[x] for x in temp])
                    - required_sessions[str(track)]
                    * add2_variables[
                        track_room_y_map[
                            self.get_problem().get_track(track).get_track_name()
                            + self.get_problem().get_room(room).get_room_name()
                        ]
                    ]
                )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0

        # Creating Constraints Eq.1
        all_constraints = []
        for z in range(self.get_problem().get_number_of_tracks()):
            for x in range(
                len(self.get_problem().get_track(z).get_track_submissions_list())
            ):
                temp = track_submission_x_map[
                    self.get_problem().get_track(z).get_track_name()
                    + self.get_problem()
                    .get_track(z)
                    .get_track_submissions_list()[x]
                    .get_submission_name()
                ]
                all_constraints.append(lpSum([variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        t_b = round((time() - t_b), 2)
        # Solving
        t_s = time()
        model.solve(GUROBI(msg=0, MIPGap=0, timeLimit=timelimit))
        # model.solve(GLPK_CMD(msg = 0))
        print("Building time:", t_b)
        print("Solving time:", round((time() - t_s), 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        """if LpStatus[model.status] == "Infeasible":
            sys.exit(print("Model is Infeasible."))"""
        solution = []
        for i in model.variables():
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
            self.get_solution().getSolTracks()[
                self.get_problem().get_session_index(solution[i][1])
            ][
                self.get_problem().get_room_index(solution[i][2])
            ] = self.get_problem().get_track_index(solution[i][3])
            ts = (
                self.get_solution()
                .getSolSubmissions()[
                    self.get_problem().get_session_index(solution[i][1])
                ][self.get_problem().get_room_index(solution[i][2])]
                .index(-1)
            )
            self.get_solution().getSolSubmissions()[
                self.get_problem().get_session_index(solution[i][1])
            ][self.get_problem().get_room_index(solution[i][2])][
                ts
            ] = self.get_problem().get_submission_index(solution[i][4])
        for sub in range(self.get_problem().get_number_of_submissions()):
            for session in range(len(self.get_solution().getSolSubmissions())):
                for room in range(
                    len(self.get_solution().getSolSubmissions()[session])
                ):
                    if sub in self.get_solution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(
                            len(self.get_solution().getSolSubmissions()[session][room])
                        ):
                            if (
                                self.get_solution().getSolSubmissions()[session][room][
                                    i
                                ]
                                != -1
                            ):
                                if (
                                    self.get_solution().getSolSubmissions()[session][
                                        room
                                    ][i]
                                    not in info
                                ):
                                    info.append(
                                        self.get_solution().getSolSubmissions()[
                                            session
                                        ][room][i]
                                    )
                        temp = []
                        for i in range(len(info)):
                            while (
                                temp.count(info[i])
                                < self.get_problem()
                                .get_submission(info[i])
                                .get_submission_required_time_slots()
                            ):
                                temp.append(info[i])
                        while len(temp) < len(
                            self.get_solution().getSolSubmissions()[session][room]
                        ):
                            temp.append(-1)
                        self.get_solution().getSolSubmissions()[session][room] = temp


class ExtendedModel(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)

    def solve(self, timelimit=3600):
        t_b = time()
        model = LpProblem("model", LpMinimize)
        names = []
        submission_conflict_x_list = []
        submission_att_conflict_x_list = []
        track_session_room_x_map = {}
        track_submission_x_map = {
            self.get_problem().get_track(track).get_track_name()
            + self.get_problem()
            .get_track(track)
            .get_track_submissions_list()[sub]
            .get_submission_name(): []
            for track in range(self.get_problem().get_number_of_tracks())
            for sub in range(
                len(self.get_problem().get_track(track).get_track_submissions_list())
            )
        }
        add_names = []
        session_room_z_map = {}
        track_session_room_z_map = {}
        room_track_z_map = {
            self.get_problem().get_room(room).get_room_name()
            + self.get_problem().get_track(track).get_track_name(): []
            for room in range(self.get_problem().get_number_of_rooms())
            for track in range(self.get_problem().get_number_of_tracks())
        }
        similar_tracks = {
            self.get_problem().get_session(session).get_session_name()
            + self.get_problem().get_track(track).get_track_name(): []
            for session in range(self.get_problem().get_number_of_sessions())
            for track in range(self.get_problem().get_number_of_tracks())
        }
        add2_names = []
        track_y_map = {}
        track_room_y_map = {}
        product_names = []
        coefficients = {}
        timeslots = {}

        # Determine MaxS for each track
        sessions_ts = []
        required_sessions = {}
        for session in range(self.get_problem().get_number_of_sessions()):
            sessions_ts.append(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        sorted_sessions_ts = sorted(sessions_ts)
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = []
            i = -1
            while self.get_problem().get_track(
                track
            ).get_track_required_time_slots() > sum(temp):
                i += 1
                temp.append(sorted_sessions_ts[i])
                if i == self.get_problem().get_number_of_sessions() - 1:
                    break
            required_sessions[str(track)] = len(temp)

        # Creating decision variables [X Variables]
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                for z in range(self.get_problem().get_number_of_tracks()):
                    temp = []
                    for x in range(
                        len(
                            self.get_problem().get_track(z).get_track_submissions_list()
                        )
                    ):
                        names.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        coefficients[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        ] = (
                            self.get_problem()
                            .get_parameters()
                            .submissions_timezones_penalty_weight
                            * self.get_problem().get_submissions_timezones_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_session(i).get_session_name(),
                            )
                            + self.get_problem()
                            .get_parameters()
                            .submissions_sessions_penalty_weight
                            * self.get_problem().get_submissions_sessions_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_session(i).get_session_name(),
                            )
                            + self.get_problem()
                            .get_parameters()
                            .submissions_rooms_penalty_weight
                            * self.get_problem().get_submissions_rooms_penalty(
                                str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                ),
                                self.get_problem().get_room(j).get_room_name(),
                            )
                        )
                        timeslots[
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        ] = (
                            self.get_problem()
                            .get_submission(
                                self.get_problem().get_submission_index(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                )
                            )
                            .get_submission_required_time_slots()
                        )
                        temp.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        track_submission_x_map[
                            self.get_problem().get_track(z).get_track_name()
                            + self.get_problem()
                            .get_track(z)
                            .get_track_submissions_list()[x]
                            .get_submission_name()
                        ].append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                            + "|"
                            + str(
                                self.get_problem()
                                .get_track(z)
                                .get_track_submissions_list()[x]
                                .get_submission_name()
                            )
                        )
                        if (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_problem().get_submission_index(
                                        self.get_problem()
                                        .get_track(z)
                                        .get_track_submissions_list()[x]
                                        .get_submission_name()
                                    )
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        ):
                            submission_conflict_x_list.append(
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + self.get_problem().get_track(z).get_track_name()
                                + "|"
                                + str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                )
                            )
                        if (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_problem().get_submission_index(
                                        self.get_problem()
                                        .get_track(z)
                                        .get_track_submissions_list()[x]
                                        .get_submission_name()
                                    )
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        ):
                            submission_att_conflict_x_list.append(
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + self.get_problem().get_track(z).get_track_name()
                                + "|"
                                + str(
                                    self.get_problem()
                                    .get_track(z)
                                    .get_track_submissions_list()[x]
                                    .get_submission_name()
                                )
                            )
                    track_session_room_x_map[
                        self.get_problem().get_track(z).get_track_name()
                        + self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_room(j).get_room_name()
                    ] = temp

        # Additional variables to minimise tracks per room [Y Variables]
        for i in range(self.get_problem().get_number_of_tracks()):
            temp = []
            for j in range(self.get_problem().get_number_of_rooms()):
                add2_names.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                temp.append(
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
                track_room_y_map[
                    self.get_problem().get_track(i).get_track_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = (
                    "|"
                    + self.get_problem().get_room(j).get_room_name()
                    + "|"
                    + self.get_problem().get_track(i).get_track_name()
                )
            track_y_map[self.get_problem().get_track(i).get_track_name()] = temp

        # Additional variables for assigning tracks into sessions and rooms [Z Variables]
        for i in range(self.get_problem().get_number_of_sessions()):
            for j in range(self.get_problem().get_number_of_rooms()):
                temp = []
                for z in range(self.get_problem().get_number_of_tracks()):
                    add_names.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    coefficients[
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    ] = (
                        self.get_problem()
                        .get_parameters()
                        .tracks_sessions_penalty_weight
                        * self.get_problem().get_tracks_sessions_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_session(i).get_session_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .tracks_rooms_penalty_weight
                        * self.get_problem().get_tracks_rooms_penalty(
                            self.get_problem().get_track(z).get_track_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                        + self.get_problem()
                        .get_parameters()
                        .sessions_rooms_penalty_weight
                        * self.get_problem().get_sessions_rooms_penalty(
                            self.get_problem().get_session(i).get_session_name(),
                            self.get_problem().get_room(j).get_room_name(),
                        )
                    )
                    temp.append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    track_session_room_z_map[
                        self.get_problem().get_track(z).get_track_name()
                        + self.get_problem().get_session(i).get_session_name()
                        + self.get_problem().get_room(j).get_room_name()
                    ] = (
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    room_track_z_map[
                        self.get_problem().get_room(j).get_room_name()
                        + self.get_problem().get_track(z).get_track_name()
                    ].append(
                        "|"
                        + self.get_problem().get_session(i).get_session_name()
                        + "|"
                        + self.get_problem().get_room(j).get_room_name()
                        + "|"
                        + self.get_problem().get_track(z).get_track_name()
                    )
                    for x in range(z + 1, self.get_problem().get_number_of_tracks()):
                        if (
                            self.get_problem().get_tracks_tracks_penalty_by_index(z, x)
                            != 0
                        ):
                            if (
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + self.get_problem().get_track(z).get_track_name()
                                not in similar_tracks[
                                    self.get_problem().get_session(i).get_session_name()
                                    + self.get_problem().get_track(z).get_track_name()
                                ]
                            ):
                                similar_tracks[
                                    self.get_problem().get_session(i).get_session_name()
                                    + self.get_problem().get_track(z).get_track_name()
                                ].append(
                                    "|"
                                    + self.get_problem()
                                    .get_session(i)
                                    .get_session_name()
                                    + "|"
                                    + self.get_problem().get_room(j).get_room_name()
                                    + "|"
                                    + self.get_problem().get_track(z).get_track_name()
                                )
                            if (
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + self.get_problem().get_track(x).get_track_name()
                                not in similar_tracks[
                                    self.get_problem().get_session(i).get_session_name()
                                    + self.get_problem().get_track(z).get_track_name()
                                ]
                            ):
                                similar_tracks[
                                    self.get_problem().get_session(i).get_session_name()
                                    + self.get_problem().get_track(z).get_track_name()
                                ].append(
                                    "|"
                                    + self.get_problem()
                                    .get_session(i)
                                    .get_session_name()
                                    + "|"
                                    + self.get_problem().get_room(j).get_room_name()
                                    + "|"
                                    + self.get_problem().get_track(x).get_track_name()
                                )
                session_room_z_map[
                    self.get_problem().get_session(i).get_session_name()
                    + self.get_problem().get_room(j).get_room_name()
                ] = temp

        # Creating products of variables for consecutive tracks
        for i in range(
            self.get_problem().get_number_of_rooms()
            * self.get_problem().get_number_of_tracks()
        ):
            temp = []
            temp.append(add_names[i])
            for j in range(len(add_names)):
                if (
                    add_names[i].split("|")[1] != add_names[j].split("|")[1]
                    and add_names[i].split("|")[2] == add_names[j].split("|")[2]
                    and add_names[i].split("|")[3] == add_names[j].split("|")[3]
                ):
                    temp.append(add_names[j])
            for z in range(len(temp) - 1):
                temp2 = temp[z] + temp[z + 1]
                product_names.append(temp2)
                coefficients[temp2] = (
                    -self.get_problem().get_parameters().consecutive_tracks_weight
                )

        # Creating objective function and binary IP formulation
        variables = LpVariable.dicts("Variables", names, cat="Binary")
        add_variables = LpVariable.dicts("AddVariables", add_names, cat="Binary")
        add2_variables = LpVariable.dicts("Add2Variables", add2_names, cat="Binary")
        product_variables = LpVariable.dicts(
            "ProdVariables", product_names, cat="Binary"
        )
        obj_function = [variables, add_variables, product_variables]
        all_names = [names, add_names, product_names]
        model += lpSum(
            [
                coefficients[i] * obj_function[x][i]
                for x in range(len(obj_function))
                for i in all_names[x]
            ]
        )

        # Creating Constraints Eq.2
        if len(submission_conflict_x_list) != 0:
            unique_conflicts = []
            for submission in range(self.get_problem().get_number_of_submissions()):
                sub_name = (
                    self.get_problem().get_submission(submission).get_submission_name()
                )
                if (
                    len(
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_presenter_conflicts_list()
                    )
                    != 0
                ):
                    for conflict in (
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_presenter_conflicts_list()
                    ):
                        for session in range(
                            self.get_problem().get_number_of_sessions()
                        ):
                            session_name = (
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                            )
                            for room in range(self.get_problem().get_number_of_rooms()):
                                room_name = (
                                    self.get_problem().get_room(room).get_room_name()
                                )
                                current_conflict = [
                                    sub_name,
                                    conflict.get_submission_name(),
                                    session_name,
                                    room_name,
                                ]
                                M_list = [
                                    len(
                                        self.get_problem()
                                        .get_submission(submission)
                                        .get_submission_presenter_conflicts_list()
                                    )
                                    + 1,
                                    self.get_problem()
                                    .get_session(session)
                                    .get_session_max_time_slots(),
                                ]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(len(submission_conflict_x_list)):
                                        if (
                                            submission_conflict_x_list[name].split("|")[
                                                4
                                            ]
                                            == sub_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[1]
                                            == session_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[2]
                                            == room_name
                                        ):
                                            temp.append(
                                                submission_conflict_x_list[name]
                                            )
                                        if (
                                            submission_conflict_x_list[name].split("|")[
                                                4
                                            ]
                                            == conflict.get_submission_name()
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[2]
                                            != room_name
                                            and submission_conflict_x_list[name].split(
                                                "|"
                                            )[1]
                                            == session_name
                                        ):
                                            temp2.append(
                                                submission_conflict_x_list[name]
                                            )
                                    model += (
                                        lpSum([M * variables[x] for x in temp])
                                        + lpSum([variables[x] for x in temp2])
                                        <= M
                                    )

        # Creating constraints Eq.5
        all_constraints = []
        for session in range(self.get_problem().get_number_of_sessions()):
            for room in range(self.get_problem().get_number_of_rooms()):
                temp = session_room_z_map[
                    self.get_problem().get_session(session).get_session_name()
                    + self.get_problem().get_room(room).get_room_name()
                ]
                all_constraints.append(lpSum([add_variables[x] for x in temp]))
        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints Eq.6 & Eq.7
        all_constraints = []
        all_constraints2 = []
        for track in range(self.get_problem().get_number_of_tracks()):
            for session in range(self.get_problem().get_number_of_sessions()):
                for room in range(self.get_problem().get_number_of_rooms()):
                    temp = track_session_room_x_map[
                        self.get_problem().get_track(track).get_track_name()
                        + self.get_problem().get_session(session).get_session_name()
                        + self.get_problem().get_room(room).get_room_name()
                    ]
                    all_constraints.append(
                        lpSum([timeslots[x] * variables[x] for x in temp])
                        - self.get_problem()
                        .get_session(session)
                        .get_session_max_time_slots()
                        * add_variables[
                            track_session_room_z_map[
                                self.get_problem().get_track(track).get_track_name()
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_room(room).get_room_name()
                            ]
                        ]
                    )
                    all_constraints2.append(
                        lpSum([variables[x] for x in temp])
                        - add_variables[
                            track_session_room_z_map[
                                self.get_problem().get_track(track).get_track_name()
                                + self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + self.get_problem().get_room(room).get_room_name()
                            ]
                        ]
                    )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0
            model += all_constraints2[c] >= 0

        # Creating constraints Eq.3
        all_constraints = []
        for track in range(self.get_problem().get_number_of_tracks()):
            temp = track_y_map[self.get_problem().get_track(track).get_track_name()]
            all_constraints.append(lpSum([add2_variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        # Creating constraints Eq.4
        all_constraints = []
        for room in range(self.get_problem().get_number_of_rooms()):
            for track in range(self.get_problem().get_number_of_tracks()):
                temp = room_track_z_map[
                    self.get_problem().get_room(room).get_room_name()
                    + self.get_problem().get_track(track).get_track_name()
                ]
                all_constraints.append(
                    lpSum([add_variables[x] for x in temp])
                    - required_sessions[str(track)]
                    * add2_variables[
                        track_room_y_map[
                            self.get_problem().get_track(track).get_track_name()
                            + self.get_problem().get_room(room).get_room_name()
                        ]
                    ]
                )

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 0

        # Creating Constraints Eq.1
        all_constraints = []
        for z in range(self.get_problem().get_number_of_tracks()):
            for x in range(
                len(self.get_problem().get_track(z).get_track_submissions_list())
            ):
                temp = track_submission_x_map[
                    self.get_problem().get_track(z).get_track_name()
                    + self.get_problem()
                    .get_track(z)
                    .get_track_submissions_list()[x]
                    .get_submission_name()
                ]
                all_constraints.append(lpSum([variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] == 1

        # Creating Constraints Eq.13
        all_constraints = []
        for i in similar_tracks.values():
            if len(i) != 0:
                temp = i
                all_constraints.append(lpSum([add_variables[x] for x in temp]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating constraints Eq.15
        all_constraints = []
        temp2 = []
        for z in range(self.get_problem().get_number_of_tracks()):
            if len(self.get_problem().get_track(z).get_trackChairConflictsList()) != 0:
                for i in range(self.get_problem().get_number_of_sessions()):
                    temp = []
                    for j in range(self.get_problem().get_number_of_rooms()):
                        temp.append(
                            "|"
                            + self.get_problem().get_session(i).get_session_name()
                            + "|"
                            + self.get_problem().get_room(j).get_room_name()
                            + "|"
                            + self.get_problem().get_track(z).get_track_name()
                        )
                        for x in (
                            self.get_problem()
                            .get_track(z)
                            .get_trackChairConflictsList()
                        ):
                            temp.append(
                                "|"
                                + self.get_problem().get_session(i).get_session_name()
                                + "|"
                                + self.get_problem().get_room(j).get_room_name()
                                + "|"
                                + x.get_track_name()
                            )
                    if sorted(temp) not in temp2:
                        temp2.append(sorted(temp))
        for i in range(len(temp2)):
            all_constraints.append(lpSum([add_variables[x] for x in temp2[i]]))

        for c in range(len(all_constraints)):
            model += all_constraints[c] <= 1

        # Creating Constraints Eq.14
        if len(submission_att_conflict_x_list) != 0:
            unique_conflicts = []
            for submission in range(self.get_problem().get_number_of_submissions()):
                sub_name = (
                    self.get_problem().get_submission(submission).get_submission_name()
                )
                if (
                    len(
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_attendee_conflicts_list()
                    )
                    != 0
                ):
                    for conflict in (
                        self.get_problem()
                        .get_submission(submission)
                        .get_submission_attendee_conflicts_list()
                    ):
                        for session in range(
                            self.get_problem().get_number_of_sessions()
                        ):
                            session_name = (
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                            )
                            for room in range(self.get_problem().get_number_of_rooms()):
                                room_name = (
                                    self.get_problem().get_room(room).get_room_name()
                                )
                                current_conflict = [
                                    sub_name,
                                    conflict.get_submission_name(),
                                    session_name,
                                    room_name,
                                ]
                                M_list = [
                                    len(
                                        self.get_problem()
                                        .get_submission(submission)
                                        .get_submission_attendee_conflicts_list()
                                    )
                                    + 1,
                                    self.get_problem()
                                    .get_session(session)
                                    .get_session_max_time_slots(),
                                ]
                                M = min(M_list)
                                if sorted(current_conflict) not in unique_conflicts:
                                    unique_conflicts.append(sorted(current_conflict))
                                    temp = []
                                    temp2 = []
                                    for name in range(
                                        len(submission_att_conflict_x_list)
                                    ):
                                        if (
                                            submission_att_conflict_x_list[name].split(
                                                "|"
                                            )[4]
                                            == sub_name
                                            and submission_att_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                            and submission_att_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            == room_name
                                        ):
                                            temp.append(
                                                submission_att_conflict_x_list[name]
                                            )
                                        if (
                                            submission_att_conflict_x_list[name].split(
                                                "|"
                                            )[4]
                                            == conflict.get_submission_name()
                                            and submission_att_conflict_x_list[
                                                name
                                            ].split("|")[2]
                                            != room_name
                                            and submission_att_conflict_x_list[
                                                name
                                            ].split("|")[1]
                                            == session_name
                                        ):
                                            temp2.append(
                                                submission_att_conflict_x_list[name]
                                            )
                                    model += (
                                        lpSum([M * variables[x] for x in temp])
                                        + lpSum([variables[x] for x in temp2])
                                        <= M
                                    )

        # Creating constraints Eq.16 & Eq.17 & Eq.18
        all_constraints1 = []
        all_constraints2 = []
        for i in range(
            self.get_problem().get_number_of_rooms()
            * self.get_problem().get_number_of_tracks()
        ):
            temp = []
            temp.append(add_names[i])
            for j in range(len(add_names)):
                if (
                    add_names[i].split("|")[1] != add_names[j].split("|")[1]
                    and add_names[i].split("|")[2] == add_names[j].split("|")[2]
                    and add_names[i].split("|")[3] == add_names[j].split("|")[3]
                ):
                    temp.append(add_names[j])
            for z in range(len(temp) - 1):
                temp2 = temp[z] + temp[z + 1]
                all_constraints1.append(
                    product_variables[temp2]
                    - add_variables[temp[z]]
                    - add_variables[temp[z + 1]]
                )
                all_constraints2.append(
                    product_variables[temp2] - add_variables[temp[z]]
                )
                all_constraints2.append(
                    product_variables[temp2] - add_variables[temp[z + 1]]
                )

        for c in range(len(all_constraints1)):
            model += all_constraints1[c] >= -1

        for c in range(len(all_constraints2)):
            model += all_constraints2[c] <= 0

        t_b = round((time() - t_b), 2)
        # Solving
        t_s = time()
        model.solve(GUROBI(msg=1, MIPGap=0, timeLimit=timelimit, IntegralityFocus=1))
        # model.solve(GLPK_CMD(msg = 0))
        print("Building time:", t_b)
        print("Solving time:", round((time() - t_s), 2))
        print(model.objective.value())
        print("Model Status:", LpStatus[model.status])
        """if LpStatus[model.status] == "Infeasible":
            sys.exit(print("Model is Infeasible."))"""
        solution = []
        for i in model.variables():
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
            self.get_solution().getSolTracks()[
                self.get_problem().get_session_index(solution[i][1])
            ][
                self.get_problem().get_room_index(solution[i][2])
            ] = self.get_problem().get_track_index(solution[i][3])
            ts = (
                self.get_solution()
                .getSolSubmissions()[
                    self.get_problem().get_session_index(solution[i][1])
                ][self.get_problem().get_room_index(solution[i][2])]
                .index(-1)
            )
            self.get_solution().getSolSubmissions()[
                self.get_problem().get_session_index(solution[i][1])
            ][self.get_problem().get_room_index(solution[i][2])][
                ts
            ] = self.get_problem().get_submission_index(solution[i][4])
        for sub in range(self.get_problem().get_number_of_submissions()):
            for session in range(len(self.get_solution().getSolSubmissions())):
                for room in range(
                    len(self.get_solution().getSolSubmissions()[session])
                ):
                    if sub in self.get_solution().getSolSubmissions()[session][room]:
                        info = []
                        for i in range(
                            len(self.get_solution().getSolSubmissions()[session][room])
                        ):
                            if (
                                self.get_solution().getSolSubmissions()[session][room][
                                    i
                                ]
                                != -1
                            ):
                                if (
                                    self.get_solution().getSolSubmissions()[session][
                                        room
                                    ][i]
                                    not in info
                                ):
                                    info.append(
                                        self.get_solution().getSolSubmissions()[
                                            session
                                        ][room][i]
                                    )
                        temp = []
                        for i in range(len(info)):
                            while (
                                temp.count(info[i])
                                < self.get_problem()
                                .get_submission(info[i])
                                .get_submission_required_time_slots()
                            ):
                                temp.append(info[i])
                        while len(temp) < len(
                            self.get_solution().getSolSubmissions()[session][room]
                        ):
                            temp.append(-1)
                        self.get_solution().getSolSubmissions()[session][room] = temp


class HyperHeuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)

    def solve(self, start_time, run_time, rr=600):
        LLHS = [
            lambda: self.SwapTrack(),
            lambda: self.SwapSubmission(),
            lambda: self.ReverseSubmission(),
        ]
        obj_best = self.get_solution().EvaluateSolution()
        obj = obj_best
        best_Sol = self.get_solution().copyWholeSolution()
        i = 0
        t = time()
        tt = rr
        while time() - start_time < run_time:
            i += 1
            select = np.random.randint(len(LLHS))
            sol_copy = self.get_solution().copyWholeSolution()
            LLHS[select]()
            self.get_solution().resetSolSubmissions()
            self.get_solution().convertSol()
            if self.get_solution().EvaluateAllSubmissionsScheduled() == True:
                obj_new = self.get_solution().QuickEvaluateSolution(obj)
                if obj_new <= obj:
                    obj = obj_new
                    if obj_new < obj_best:
                        best_Sol = self.get_solution().copyWholeSolution()
                        obj_best = obj_new
                else:
                    self.get_solution().restoreSolution(
                        sol_copy[0], sol_copy[1], sol_copy[2]
                    )
            else:
                self.get_solution().restoreSolution(
                    sol_copy[0], sol_copy[1], sol_copy[2]
                )
            # Ruin & Recreate
            if time() - t > tt:
                s = 0
                while s != 10:
                    sol_copy = self.get_solution().copyWholeSolution()
                    LLHS[0]()
                    self.get_solution().resetSolSubmissions()
                    self.get_solution().convertSol()
                    if self.get_solution().EvaluateAllSubmissionsScheduled() == False:
                        self.get_solution().restoreSolution(
                            sol_copy[0], sol_copy[1], sol_copy[2]
                        )
                    else:
                        s += 1
                obj = self.get_solution().EvaluateSolution()
                tt += rr
        self.get_solution().setBestSolution(best_Sol[0], best_Sol[1])
        print("Number of iterations:", i)


class Matheuristic(Optimisation):
    def __init__(self, problem, solution):
        Optimisation.__init__(self, problem, solution)

    def solve(self, start_time, run_time, timelimit=90):
        self.TracksExactModel(timelimit)
        self.get_solution().convertIndSolFirstTime()
        solver = HyperHeuristic(self.get_problem(), self.get_solution())
        solver.solve(start_time, run_time)

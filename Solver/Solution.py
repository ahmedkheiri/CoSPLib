# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
import numpy as np
import pandas as pd


class Solution:
    def __init__(self, problem):
        self.__problem = problem
        self.__solTracks = [
            [-1 for x in range(self.getProblem().get_number_of_rooms())]
            for y in range(self.getProblem().get_number_of_sessions())
        ]
        self.__solSubmissions = [
            [
                [
                    -1
                    for x in range(
                        self.getProblem().get_session(z).get_session_max_time_slots()
                    )
                ]
                for y in range(self.getProblem().get_number_of_rooms())
            ]
            for z in range(self.getProblem().get_number_of_sessions())
        ]
        self.__indsolSubmissions = [
            [
                self.getProblem().get_submission_index(x.get_submission_name())
                for x in self.getProblem().get_track(y).get_track_submissions_list()
            ]
            for y in range(self.getProblem().get_number_of_tracks())
        ]
        self.generateEvaluations()

    def getProblem(self) -> Problem:
        return self.__problem

    def getSolTracks(self) -> list:
        return self.__solTracks

    def getSolSubmissions(self) -> list:
        return self.__solSubmissions

    def getIndSolSubmissions(self) -> list:
        return self.__indsolSubmissions

    def setIndSolSubmissions(self, solInd):
        self.__indsolSubmissions = solInd

    def setBestSolution(self, solTracks, solSubmissions):
        self.__solTracks = solTracks
        self.__solSubmissions = solSubmissions

    def restoreSolution(self, solTracks, solSubmissions, solInd):
        self.__solTracks = solTracks
        self.__solSubmissions = solSubmissions
        self.__indsolSubmissions = solInd

    def resetSolTracks(self):
        self.__solTracks = [
            [-1 for x in range(self.getProblem().get_number_of_rooms())]
            for y in range(self.getProblem().get_number_of_sessions())
        ]

    def resetSolSubmissions(self):
        self.__solSubmissions = [
            [
                [
                    -1
                    for x in range(
                        self.getProblem().get_session(z).get_session_max_time_slots()
                    )
                ]
                for y in range(self.getProblem().get_number_of_rooms())
            ]
            for z in range(self.getProblem().get_number_of_sessions())
        ]

    def resetIndSolSubmissions(self):
        self.__indsolSubmissions = [
            [
                self.getProblem().get_submission_index(x.get_submission_name())
                for x in self.getProblem().get_track(y).get_track_submissions_list()
            ]
            for y in range(self.getProblem().get_number_of_tracks())
        ]

    def generateEvaluations(self):
        self.__evaluations = []
        self.__evaluations_names = {}
        if self.getProblem().get_parameters().tracks_sessions_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().tracks_sessions_penalty_weight
                    * self.EvaluateTracksSessions()
                ),
                "Tracks_Sessions|Penalty:",
            )
        if self.getProblem().get_parameters().tracks_rooms_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().tracks_rooms_penalty_weight
                    * self.EvaluateTracksRooms()
                ),
                "Tracks_Rooms|Penalty:",
            )
        if self.getProblem().get_parameters().sessions_rooms_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().sessions_rooms_penalty_weight
                    * self.EvaluateSessionsRooms()
                ),
                "Sessions_Rooms|Penalty",
            )
        if self.getProblem().get_parameters().similar_tracks_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().similar_tracks_penalty_weight
                    * self.EvaluateSimilarTracks()
                ),
                "Similar Tracks:",
            )
        if self.getProblem().get_parameters().num_rooms_per_track_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().num_rooms_per_track_weight
                    * self.EvaluateNumberOfRoomsPerTrack()
                ),
                "Number of rooms per track:",
            )
        if self.getProblem().get_parameters().parallel_tracks_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().parallel_tracks_weight
                    * self.EvaluateParallelTracks()
                ),
                "Parallel tracks:",
            )
        if self.getProblem().get_parameters().consecutive_tracks_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().consecutive_tracks_weight
                    * self.EvaluateConsecutiveTracks()
                ),
                "Consecutive tracks:",
            )
        if self.getProblem().get_parameters().submissions_timezones_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem()
                    .get_parameters()
                    .submissions_timezones_penalty_weight
                    * self.EvaluateSubmissionsTimezones()
                ),
                "Submissions timezones:",
            )
        if self.getProblem().get_parameters().submissions_order_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().submissions_order_weight
                    * self.EvaluateSubmissionsOrder()
                ),
                "Submissions order:",
            )
        if self.getProblem().get_parameters().submissions_sessions_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem()
                    .get_parameters()
                    .submissions_sessions_penalty_weight
                    * self.EvaluateSubmissionsSessions()
                ),
                "Submissions_Sessions|Penalty:",
            )
        if self.getProblem().get_parameters().submissions_rooms_penalty_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().submissions_rooms_penalty_weight
                    * self.EvaluateSubmissionsRooms()
                ),
                "Submissions_Rooms|Penalty:",
            )
        if self.getProblem().get_parameters().presenters_conflicts_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().presenters_conflicts_weight
                    * self.EvaluatePresentersConflicts()
                ),
                "Presenters conflicts [Session Level]:",
            )
        if self.getProblem().get_parameters().attendees_conflicts_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().attendees_conflicts_weight
                    * self.EvaluateAttendeesConflicts()
                ),
                "Attendees conflicts [Session Level]:",
            )
        if self.getProblem().get_parameters().chairs_conflicts_weight > 0:
            self.setEvaluation(
                lambda: (
                    self.getProblem().get_parameters().chairs_conflicts_weight
                    * self.EvaluateChairsConflicts()
                ),
                "Chairs conflicts:",
            )
        if (
            self.getProblem()
            .get_parameters()
            .presenters_conflicts_timeslot_level_weight
            > 0
        ):
            self.setEvaluation(
                lambda: (
                    self.getProblem()
                    .get_parameters()
                    .presenters_conflicts_timeslot_level_weight
                    * self.EvaluatePresentersConflictsTS()
                ),
                "Presenters conflicts [Timeslot Level]:",
            )
        if (
            self.getProblem().get_parameters().attendees_conflicts_timeslot_level_weight
            > 0
        ):
            self.setEvaluation(
                lambda: (
                    self.getProblem()
                    .get_parameters()
                    .attendees_conflicts_timeslot_level_weight
                    * self.EvaluateAttendeesConflictsTS()
                ),
                "Attendees conflicts [Timeslot Level]:",
            )
        self.setEvaluation(
            lambda: self.EvaluateExtendedSubmissions(),
            "Submissions with multiple timeslots in different sessions:",
        )

    def setEvaluation(self, evaluation_function, evaluation_name):
        self.__evaluations.append(evaluation_function)
        self.__evaluations_names[evaluation_function] = evaluation_name

    def getEvaluationsList(self) -> list:
        return self.__evaluations

    def getEvaluationName(self, evaluation_function) -> str:
        return self.__evaluations_names[evaluation_function]

    def EvaluateTracksSessions(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().get_tracks_sessions_penalty_by_index(
                        self.getSolTracks()[i][j], i
                    )
        return pen

    def EvaluateTracksRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().get_tracks_rooms_penalty_by_index(
                        self.getSolTracks()[i][j], j
                    )
        return pen

    def EvaluateSessionsRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    pen += self.getProblem().get_sessions_rooms_penalty_by_index(i, j)
        return pen

    def EvaluateSimilarTracks(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (
                        (self.getSolTracks()[i][j] != self.getSolTracks()[i][x])
                        and (self.getSolTracks()[i][j] != -1)
                        and (self.getSolTracks()[i][x] != -1)
                    ):
                        pen += self.getProblem().get_tracks_tracks_penalty_by_index(
                            self.getSolTracks()[i][j], self.getSolTracks()[i][x]
                        )
        return pen

    def EvaluateNumberOfRoomsPerTrack(self) -> int:
        pen = 0
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    j not in di[self.getSolTracks()[i][j]]
                ):
                    di[self.getSolTracks()[i][j]].append(j)
        for i in di.values():
            if len(i) > 1:
                pen += len(i) - 1
        return pen

    def EvaluateParallelTracks(self) -> int:
        pen = 0
        temp = [
            tuple(self.getSolTracks()[session])
            for session in range(len(self.getSolTracks()))
        ]
        for track in range(self.getProblem().get_number_of_tracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    pen += c - 1
        return pen

    def EvaluateConsecutiveTracks(self) -> int:
        pen = 0
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    i not in di[self.getSolTracks()[i][j]]
                ):
                    di[self.getSolTracks()[i][j]].append(i)
        for i in di.values():
            if (len(i) > 1) and (sum(i) != sum(range(i[0], i[len(i) - 1] + 1))):
                pen += 1
        return pen

    def EvaluateSubmissionsTimezones(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().get_submissions_timezones_penalty_by_index(
                            self.getSolSubmissions()[i][j][x], i
                        )
        return pen

    def EvaluateSubmissionsOrder(self) -> int:
        pen = 0
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        session_ts = {
            self.getProblem().get_session(session).get_session_name() + str(ts): []
            for session in range(len(self.getSolTracks()))
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[self.getSolTracks()[session][room]]
                        ):
                            di[self.getSolTracks()[session][room]].append(
                                self.getSolSubmissions()[session][room][ts]
                            )
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (
                            self.getSolSubmissions()[session][room][ts]
                            not in session_ts[
                                self.getProblem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ]
                        ):
                            session_ts[
                                self.getProblem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ].append(self.getSolSubmissions()[session][room][ts])

        for ts in session_ts.values():
            for this_sub in range(len(ts) - 1):
                for other_sub in range(this_sub + 1, len(ts)):
                    if (
                        self.getProblem()
                        .get_submission(ts[this_sub])
                        .get_submission_track()
                        .get_track_name()
                        == self.getProblem()
                        .get_submission(ts[other_sub])
                        .get_submission_track()
                        .get_track_name()
                    ) and (
                        (
                            self.getProblem()
                            .get_submission(ts[this_sub])
                            .get_submission_order()
                            != 0
                        )
                        and (
                            self.getProblem()
                            .get_submission(ts[other_sub])
                            .get_submission_order()
                            != 0
                        )
                    ):
                        pen += 1

        for track in range(self.getProblem().get_number_of_tracks()):
            order = 1
            for sub in di[track]:
                if (
                    self.getProblem().get_submission(sub).get_submission_order()
                    != order
                ) and (
                    self.getProblem().get_submission(sub).get_submission_order() != 0
                ):
                    pen += 1
                order += 1
        return pen

    def EvaluateSubmissionsSessions(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += (
                            self.getProblem().get_submissions_sessions_penalty_by_index(
                                self.getSolSubmissions()[i][j][x], i
                            )
                        )
        return pen

    def EvaluateSubmissionsRooms(self) -> int:
        pen = 0
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        pen += self.getProblem().get_submissions_rooms_penalty_by_index(
                            self.getSolSubmissions()[i][j][x], j
                        )
        return pen

    def EvaluatePresentersConflicts(self) -> int:  # Session Level
        pen = 0
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (
                        (self.getSolSubmissions()[i][j][x] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.getSolSubmissions()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_submission(di[i][j][0])
                            in self.getProblem()
                            .get_submission(di[i][z][0])
                            .get_submission_presenter_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen

    def EvaluateAttendeesConflicts(self) -> int:  # Session Level
        pen = 0
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (
                        (self.getSolSubmissions()[i][j][x] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.getSolSubmissions()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_submission(di[i][j][0])
                            in self.getProblem()
                            .get_submission(di[i][z][0])
                            .get_submission_attendee_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            pen += 1
        return pen

    def EvaluateChairsConflicts(self) -> int:
        pen = 0
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    len(
                        self.getProblem()
                        .get_track(self.getSolTracks()[i][j])
                        .get_track_chair_conflicts_list()
                    )
                    != 0
                ):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_track(di[i][j])
                            in self.getProblem()
                            .get_track(di[i][z])
                            .get_track_chair_conflicts_list()
                        ):
                            pen += 1
        return pen

    def EvaluatePresentersConflictsTS(self) -> int:  # Time slot Level
        pen = 0
        di = {
            str(session) + str(ts): []
            for session in range(self.getProblem().get_number_of_sessions())
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (
                        (self.getSolSubmissions()[session][room][ts] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(
                                    self.getSolSubmissions()[session][room][ts]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.getSolSubmissions()[session][room][ts]
                        )
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.getProblem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.getProblem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_presenter_conflicts_list()
                            ):
                                pen += 1
        return pen

    def EvaluateAttendeesConflictsTS(self) -> int:  # Time slot level
        pen = 0
        di = {
            str(session) + str(ts): []
            for session in range(self.getProblem().get_number_of_sessions())
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (
                        (self.getSolSubmissions()[session][room][ts] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(
                                    self.getSolSubmissions()[session][room][ts]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.getSolSubmissions()[session][room][ts]
                        )
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.getProblem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.getProblem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_attendee_conflicts_list()
                            ):
                                pen += 1
        return pen

    def EvaluateExtendedSubmissions(self) -> int:
        pen = 0
        di = {
            str(session) + str(room): []
            for session in range(self.getProblem().get_number_of_sessions())
            for room in range(self.getProblem().get_number_of_rooms())
        }
        di2 = {
            sub: []
            for sub in range(self.getProblem().get_number_of_submissions())
            if self.getProblem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            > 1
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (self.getSolSubmissions()[session][room][ts] != -1) and (
                        self.getProblem()
                        .get_submission(self.getSolSubmissions()[session][room][ts])
                        .get_submission_required_time_slots()
                        > 1
                    ):
                        di[str(session) + str(room)].append(
                            self.getSolSubmissions()[session][room][ts]
                        )
                        di2[self.getSolSubmissions()[session][room][ts]].append(ts)
        for i in di.values():
            if len(i) != 0:
                temp = set(i)
                for j in temp:
                    if self.getProblem().get_submission(
                        j
                    ).get_submission_required_time_slots() != i.count(j):
                        pen += 10000000
        for i in di2.values():
            if len(i) == 0:
                pen += 1000000000
                return pen
            if sum(range(i[0], i[len(i) - 1] + 1)) != sum(i):
                pen += 1000000000
        return pen

    def EvaluateAllSubmissionsScheduled(self) -> bool:
        temp = [
            self.getSolSubmissions()[session][room][ts]
            for session in range(len(self.getSolTracks()))
            for room in range(len(self.getSolTracks()[session]))
            for ts in range(len(self.getSolSubmissions()[session][room]))
            if self.getSolSubmissions()[session][room][ts] != -1
        ]
        for sub in range(self.getProblem().get_number_of_submissions()):
            if (sub not in temp) or (
                self.getProblem()
                .get_submission(sub)
                .get_submission_required_time_slots()
                != temp.count(sub)
            ):
                return False
        return True

    def ValidateSolution(self) -> bool:
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolTracks()[i][j] != -1:
                        if self.getSolSubmissions()[i][j][x] != -1:
                            if (
                                self.getProblem().get_submission(
                                    self.getSolSubmissions()[i][j][x]
                                )
                                not in self.getProblem()
                                .get_track(self.getSolTracks()[i][j])
                                .get_track_submissions_list()
                            ):
                                return False
        return True

    def EvaluateSolution(self) -> int:
        obj = [
            self.getEvaluationsList()[i]()
            for i in range(len(self.getEvaluationsList()))
        ]
        return sum(obj)

    def QuickEvaluateSolution(self, previous_obj) -> int:
        obj = 0
        for i in range(len(self.getEvaluationsList())):
            obj += self.getEvaluationsList()[i]()
            if obj > previous_obj:
                return obj
        return obj

    def copyWholeSolution(self):
        copy_solTracks = []
        copy_solSubmissions = []
        for i in range(len(self.getSolTracks())):
            temp = []
            temp3 = []
            for j in range(len(self.getSolTracks()[i])):
                temp.append(self.getSolTracks()[i][j])
                temp2 = []
                for z in range(len(self.getSolSubmissions()[i][j])):
                    temp2.append(self.getSolSubmissions()[i][j][z])
                temp3.append(temp2)
            copy_solTracks.append(temp)
            copy_solSubmissions.append(temp3)
        copy_indsol = []
        for i in range(len(self.getIndSolSubmissions())):
            temp = []
            for j in range(len(self.getIndSolSubmissions()[i])):
                temp.append(self.getIndSolSubmissions()[i][j])
            copy_indsol.append(temp)
        return copy_solTracks, copy_solSubmissions, copy_indsol

    def convertIndSolFirstTime(self):
        temp = [
            self.getIndSolSubmissions()[track][sub]
            for track in range(len(self.getIndSolSubmissions()))
            for sub in range(len(self.getIndSolSubmissions()[track]))
        ]
        for sub in temp:
            if (
                self.getProblem()
                .get_submission(sub)
                .get_submission_required_time_slots()
                == 1
            ):
                stop = False
                for session in range(self.getProblem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.getProblem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.getProblem()
                            .get_submission(sub)
                            .get_submission_required_time_slots()
                            <= self.getSolSubmissions()[session][room].count(-1)
                        ) and (
                            self.getProblem().get_track_index(
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.getSolTracks()[session][room]
                        ):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
        for session in range(self.getProblem().get_number_of_sessions()):
            for room in range(self.getProblem().get_number_of_rooms()):
                if self.getSolSubmissions()[session][room].count(-1) == len(
                    self.getSolSubmissions()[session][room]
                ):
                    self.getSolTracks()[session][room] = -1
        # Creating Ind sol
        temp3 = [[] for i in range(self.getProblem().get_number_of_tracks())]
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    for x in range(len(self.getSolSubmissions()[i][j])):
                        if (self.getSolSubmissions()[i][j][x] != -1) and (
                            self.getSolSubmissions()[i][j][x]
                            not in temp3[self.getSolTracks()[i][j]]
                        ):
                            temp3[self.getSolTracks()[i][j]].append(
                                self.getSolSubmissions()[i][j][x]
                            )
        self.setIndSolSubmissions(temp3)

    def convertSol(self):
        temp = [
            self.getIndSolSubmissions()[track][sub]
            for track in range(len(self.getIndSolSubmissions()))
            for sub in range(len(self.getIndSolSubmissions()[track]))
        ]
        for sub in temp:
            if (
                self.getProblem()
                .get_submission(sub)
                .get_submission_required_time_slots()
                > 1
            ):
                stop = False
                for session in range(self.getProblem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.getProblem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.getProblem()
                            .get_submission(sub)
                            .get_submission_required_time_slots()
                            <= self.getSolSubmissions()[session][room].count(-1)
                        ) and (
                            self.getProblem().get_track_index(
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.getSolTracks()[session][room]
                        ):
                            for ts in range(
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                            ):
                                i = self.getSolSubmissions()[session][room].index(-1)
                                self.getSolSubmissions()[session][room][i] = sub
                            stop = True
            else:
                stop = False
                for session in range(self.getProblem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.getProblem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.getProblem()
                            .get_submission(sub)
                            .get_submission_required_time_slots()
                            <= self.getSolSubmissions()[session][room].count(-1)
                        ) and (
                            self.getProblem().get_track_index(
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.getSolTracks()[session][room]
                        ):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
        for session in range(self.getProblem().get_number_of_sessions()):
            for room in range(self.getProblem().get_number_of_rooms()):
                if self.getSolSubmissions()[session][room].count(-1) == len(
                    self.getSolSubmissions()[session][room]
                ):
                    self.getSolTracks()[session][room] = -1

    def printViolations(self):
        print("----- Violations breakdown -----")
        for i in range(len(self.getEvaluationsList())):
            result = self.getEvaluationsList()[i]()
            if result > 0:
                print(self.getEvaluationName(self.getEvaluationsList()[i]), result)
        print("--------------------------------")

    def toExcel(self, file_name="Solution.xlsx"):
        # Preparing sol tracks
        df = pd.DataFrame(
            self.getSolTracks(),
            index=[
                self.getProblem().get_session(s).get_session_name()
                for s in range(self.getProblem().get_number_of_sessions())
            ],
            columns=[
                self.getProblem().get_room(r).get_room_name()
                for r in range(self.getProblem().get_number_of_rooms())
            ],
        )
        df = df.map(
            lambda x: self.getProblem().get_track(x).get_track_name() if x != -1 else ""
        )

        # Preparing sol submissions
        temp2 = []
        for session in range(self.getProblem().get_number_of_sessions()):
            for t in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            ):
                temp = []
                for room in range(self.getProblem().get_number_of_rooms()):
                    if self.getSolSubmissions()[session][room][t] != -1:
                        temp.append(
                            self.getProblem()
                            .get_submission(self.getSolSubmissions()[session][room][t])
                            .get_submission_name()
                        )
                    else:
                        temp.append("")
                temp2.append(temp)
        df2 = pd.DataFrame(
            temp2,
            index=[
                self.getProblem().get_session(s).get_session_name()
                for s in range(self.getProblem().get_number_of_sessions())
                for t in range(
                    self.getProblem().get_session(s).get_session_max_time_slots()
                )
            ],
        )

        # Preparing objective
        obj = self.EvaluateSolution()
        obj_list = ["Obj", "Final Objective = " + str(obj)]
        df3 = pd.DataFrame(obj_list)

        # Preparing Tracks|Sessions penalty
        p1_list = ["Evaluate Tracks|Sessions"]
        p1_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if (
                        self.getProblem().get_tracks_sessions_penalty_by_index(
                            self.getSolTracks()[i][j], i
                        )
                        != 0
                    ):
                        p1_list.append(
                            self.getProblem()
                            .get_track(self.getSolTracks()[i][j])
                            .get_track_name()
                            + " - "
                            + self.getProblem().get_session(i).get_session_name()
                        )
                        p1_pen.append(
                            self.getProblem()
                            .get_parameters()
                            .tracks_sessions_penalty_weight
                            * self.getProblem().get_tracks_sessions_penalty_by_index(
                                self.getSolTracks()[i][j], i
                            )
                        )
        p1_list.append("Total")
        p1_pen.append(sum(p1_pen))
        p1_pen.insert(0, "")
        df4 = pd.DataFrame(p1_list)
        df5 = pd.DataFrame(p1_pen)

        # Preparing Tracks|Rooms penalty
        p2_list = ["Evaluate Tracks|Rooms"]
        p2_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if (
                        self.getProblem().get_tracks_rooms_penalty_by_index(
                            self.getSolTracks()[i][j], j
                        )
                        != 0
                    ):
                        p2_list.append(
                            self.getProblem()
                            .get_track(self.getSolTracks()[i][j])
                            .get_track_name()
                            + " - "
                            + self.getProblem().get_room(j).get_room_name()
                        )
                        p2_pen.append(
                            self.getProblem()
                            .get_parameters()
                            .tracks_rooms_penalty_weight
                            * self.getProblem().get_tracks_rooms_penalty_by_index(
                                self.getSolTracks()[i][j], j
                            )
                        )
        p2_list.append("Total")
        p2_pen.append(sum(p2_pen))
        p2_pen.insert(0, "")
        df6 = pd.DataFrame(p2_list)
        df7 = pd.DataFrame(p2_pen)

        # Preparing Sessions|Rooms penalty
        p3_list = ["Evaluate Sessions|Rooms"]
        p3_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if self.getSolTracks()[i][j] != -1:
                    if self.getProblem().get_sessions_rooms_penalty_by_index(i, j) != 0:
                        p3_list.append(
                            self.getProblem().get_session(i).get_session_name()
                            + " - "
                            + self.getProblem().get_room(j).get_room_name()
                        )
                        p3_pen.append(
                            self.getProblem()
                            .get_parameters()
                            .sessions_rooms_penalty_weight
                            * self.getProblem().get_sessions_rooms_penalty_by_index(
                                i, j
                            )
                        )
        p3_list.append("Total")
        p3_pen.append(sum(p3_pen))
        p3_pen.insert(0, "")
        df8 = pd.DataFrame(p3_list)
        df9 = pd.DataFrame(p3_pen)

        # Preparing Similar tracks penalty
        p4_list = ["Evaluate Similar Tracks"]
        p4_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(j, len(self.getSolTracks()[i])):
                    if (
                        (self.getSolTracks()[i][j] != self.getSolTracks()[i][x])
                        and (self.getSolTracks()[i][j] != -1)
                        and (self.getSolTracks()[i][x] != -1)
                    ):
                        if (
                            self.getProblem().get_tracks_tracks_penalty_by_index(
                                self.getSolTracks()[i][j], self.getSolTracks()[i][x]
                            )
                            != 0
                        ):
                            p4_list.append(
                                self.getProblem()
                                .get_track(self.getSolTracks()[i][j])
                                .get_track_name()
                                + " - "
                                + self.getProblem()
                                .get_track(self.getSolTracks()[i][x])
                                .get_track_name()
                                + " - "
                                + self.getProblem().get_session(i).get_session_name()
                            )
                            p4_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .similar_tracks_penalty_weight
                                * self.getProblem().get_tracks_tracks_penalty_by_index(
                                    self.getSolTracks()[i][j], self.getSolTracks()[i][x]
                                )
                            )
        p4_list.append("Total")
        p4_pen.append(sum(p4_pen))
        p4_pen.insert(0, "")
        df10 = pd.DataFrame(p4_list)
        df11 = pd.DataFrame(p4_pen)

        # Preparing Number of rooms per track
        p5_list = ["Evaluate NumberOfRoomsPerTrack"]
        p5_pen = []
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    j not in di[self.getSolTracks()[i][j]]
                ):
                    di[self.getSolTracks()[i][j]].append(j)
        t = -1
        for i in di.values():
            t += 1
            if len(i) > 1:
                p5_list.append(self.getProblem().get_track(t).get_track_name())
                p5_pen.append(
                    self.getProblem().get_parameters().num_rooms_per_track_weight
                    * (len(i) - 1)
                )
        p5_list.append("Total")
        p5_pen.append(sum(p5_pen))
        p5_pen.insert(0, "")
        df12 = pd.DataFrame(p5_list)
        df13 = pd.DataFrame(p5_pen)

        # Preparing Parallel tracks
        p6_list = ["Evaluate Parallel Tracks"]
        p6_pen = []
        temp = [
            tuple(self.getSolTracks()[session])
            for session in range(len(self.getSolTracks()))
        ]
        for track in range(self.getProblem().get_number_of_tracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    p6_list.append(
                        self.getProblem().get_track(track).get_track_name()
                        + " - "
                        + self.getProblem().get_session(session).get_session_name()
                    )
                    p6_pen.append(
                        self.getProblem().get_parameters().parallel_tracks_weight
                        * (c - 1)
                    )
        p6_list.append("Total")
        p6_pen.append(sum(p6_pen))
        p6_pen.insert(0, "")
        df14 = pd.DataFrame(p6_list)
        df15 = pd.DataFrame(p6_pen)

        # Preparing Consecutive Tracks
        p7_list = ["Evaluate Consecutive Tracks"]
        p7_pen = []
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    i not in di[self.getSolTracks()[i][j]]
                ):
                    di[self.getSolTracks()[i][j]].append(i)
        t = -1
        for i in di.values():
            t += 1
            if (len(i) > 1) and (sum(i) != sum(range(i[0], i[len(i) - 1] + 1))):
                p7_list.append(self.getProblem().get_track(t).get_track_name())
                p7_pen.append(
                    self.getProblem().get_parameters().consecutive_tracks_weight
                )
        p7_list.append("Total")
        p7_pen.append(sum(p7_pen))
        p7_pen.insert(0, "")
        df16 = pd.DataFrame(p7_list)
        df17 = pd.DataFrame(p7_pen)

        # Preparing Submissions|Timezones penalty
        p9_list = ["Evaluate Submissions|Timezones"]
        p9_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if (
                            self.getProblem().get_submissions_timezones_penalty_by_index(
                                self.getSolSubmissions()[i][j][x], i
                            )
                            != 0
                        ):
                            p9_list.append(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_name()
                                + " - "
                                + self.getProblem().get_session(i).get_session_name()
                            )
                            p9_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .submissions_timezones_penalty_weight
                                * self.getProblem().get_submissions_timezones_penalty_by_index(
                                    self.getSolSubmissions()[i][j][x], i
                                )
                            )
        p9_list.append("Total")
        p9_pen.append(sum(p9_pen))
        p9_pen.insert(0, "")
        df20 = pd.DataFrame(p9_list)
        df21 = pd.DataFrame(p9_pen)

        # Preparing Submissions Order
        p11_list = ["Evaluate Submissions Order"]
        p11_pen = []
        di = {track: [] for track in range(self.getProblem().get_number_of_tracks())}
        session_ts = {
            self.getProblem().get_session(session).get_session_name() + str(ts): []
            for session in range(len(self.getSolTracks()))
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }

        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                if self.getSolTracks()[session][room] != -1:
                    for ts in range(len(self.getSolSubmissions()[session][room])):
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[self.getSolTracks()[session][room]]
                        ):
                            di[self.getSolTracks()[session][room]].append(
                                self.getSolSubmissions()[session][room][ts]
                            )
                        if (self.getSolSubmissions()[session][room][ts] != -1) and (
                            self.getSolSubmissions()[session][room][ts]
                            not in session_ts[
                                self.getProblem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ]
                        ):
                            session_ts[
                                self.getProblem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ].append(self.getSolSubmissions()[session][room][ts])

        for ts in session_ts.values():
            for this_sub in range(len(ts) - 1):
                for other_sub in range(this_sub + 1, len(ts)):
                    if (
                        self.getProblem()
                        .get_submission(ts[this_sub])
                        .get_submission_track()
                        .get_track_name()
                        == self.getProblem()
                        .get_submission(ts[other_sub])
                        .get_submission_track()
                        .get_track_name()
                    ) and (
                        (
                            self.getProblem()
                            .get_submission(ts[this_sub])
                            .get_submission_order()
                            != 0
                        )
                        and (
                            self.getProblem()
                            .get_submission(ts[other_sub])
                            .get_submission_order()
                            != 0
                        )
                    ):
                        p11_list.append(
                            self.getProblem()
                            .get_submission(ts[this_sub])
                            .get_submission_name()
                        )
                        p11_pen.append(
                            self.getProblem().get_parameters().submissions_order_weight
                        )

        for track in range(self.getProblem().get_number_of_tracks()):
            order = 1
            for sub in di[track]:
                if (
                    self.getProblem().get_submission(sub).get_submission_order()
                    != order
                ) and (
                    self.getProblem().get_submission(sub).get_submission_order() != 0
                ):
                    p11_list.append(
                        self.getProblem().get_submission(sub).get_submission_name()
                    )
                    p11_pen.append(
                        self.getProblem().get_parameters().submissions_order_weight
                    )
                order += 1
        p11_list.append("Total")
        p11_pen.append(sum(p11_pen))
        p11_pen.insert(0, "")
        df24 = pd.DataFrame(p11_list)
        df25 = pd.DataFrame(p11_pen)

        # Preparing Submissions|Sessions penalty
        p12_list = ["Evaluate Submissions|Sessions"]
        p12_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if (
                            self.getProblem().get_submissions_sessions_penalty_by_index(
                                self.getSolSubmissions()[i][j][x], i
                            )
                            != 0
                        ):
                            p12_list.append(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_name()
                                + " - "
                                + self.getProblem().get_session(i).get_session_name()
                            )
                            p12_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .submissions_sessions_penalty_weight
                                * self.getProblem().get_submissions_sessions_penalty_by_index(
                                    self.getSolSubmissions()[i][j][x], i
                                )
                            )
        p12_list.append("Total")
        p12_pen.append(sum(p12_pen))
        p12_pen.insert(0, "")
        df26 = pd.DataFrame(p12_list)
        df27 = pd.DataFrame(p12_pen)

        # Preparing Submissions|Rooms penalty
        p13_list = ["Evaluate Submissions|Rooms"]
        p13_pen = []
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if self.getSolSubmissions()[i][j][x] != -1:
                        if (
                            self.getProblem().get_submissions_rooms_penalty_by_index(
                                self.getSolSubmissions()[i][j][x], j
                            )
                            != 0
                        ):
                            p13_list.append(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_name()
                                + " - "
                                + self.getProblem().get_room(j).get_room_name()
                            )
                            p13_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .submissions_rooms_penalty_weight
                                * self.getProblem().get_submissions_rooms_penalty_by_index(
                                    self.getSolSubmissions()[i][j][x], j
                                )
                            )
        p13_list.append("Total")
        p13_pen.append(sum(p13_pen))
        p13_pen.insert(0, "")
        df28 = pd.DataFrame(p13_list)
        df29 = pd.DataFrame(p13_pen)

        # Preparing Presenters Conflicts [S]
        p14_list = ["Evaluate Presenters Conflicts [S]"]
        p14_pen = []
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (
                        (self.getSolSubmissions()[i][j][x] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.getSolSubmissions()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_submission(di[i][j][0])
                            in self.getProblem()
                            .get_submission(di[i][z][0])
                            .get_submission_presenter_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            p14_list.append(
                                str(
                                    self.getProblem()
                                    .get_submission(di[i][j][0])
                                    .get_submission_name()
                                )
                                + " - "
                                + str(
                                    self.getProblem()
                                    .get_submission(di[i][z][0])
                                    .get_submission_name()
                                )
                            )
                            p14_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .presenters_conflicts_weight
                            )
        p14_list.append("Total")
        p14_pen.append(sum(p14_pen))
        p14_pen.insert(0, "")
        df30 = pd.DataFrame(p14_list)
        df31 = pd.DataFrame(p14_pen)

        # Preparing Attendees Conflicts [S]
        p15_list = ["Evaluate Attendees Conflicts [S]"]
        p15_pen = []
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                for x in range(len(self.getSolSubmissions()[i][j])):
                    if (
                        (self.getSolSubmissions()[i][j][x] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(self.getSolSubmissions()[i][j][x])
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.getSolSubmissions()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.getSolSubmissions()[i][j][x], j))
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_submission(di[i][j][0])
                            in self.getProblem()
                            .get_submission(di[i][z][0])
                            .get_submission_attendee_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            p15_list.append(
                                self.getProblem()
                                .get_submission(di[i][j][0])
                                .get_submission_name()
                                + " - "
                                + self.getProblem()
                                .get_submission(di[i][z][0])
                                .get_submission_name()
                            )
                            p15_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .attendees_conflicts_weight
                            )
        p15_list.append("Total")
        p15_pen.append(sum(p15_pen))
        p15_pen.insert(0, "")
        df32 = pd.DataFrame(p15_list)
        df33 = pd.DataFrame(p15_pen)

        # Preparing Chairs Conflicts
        p16_list = ["Evaluate Chairs Conflicts"]
        p16_pen = []
        di = {
            session: [] for session in range(self.getProblem().get_number_of_sessions())
        }
        for i in range(len(self.getSolTracks())):
            for j in range(len(self.getSolTracks()[i])):
                if (self.getSolTracks()[i][j] != -1) and (
                    len(
                        self.getProblem()
                        .get_track(self.getSolTracks()[i][j])
                        .get_track_chair_conflicts_list()
                    )
                    != 0
                ):
                    di[i].append(self.getSolTracks()[i][j])
        for i in range(len(self.getSolTracks())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.getProblem().get_track(di[i][j])
                            in self.getProblem()
                            .get_track(di[i][z])
                            .get_track_chair_conflicts_list()
                        ):
                            p16_list.append(
                                self.getProblem().get_track(di[i][j]).get_track_name()
                                + " - "
                                + self.getProblem().get_track(di[i][z]).get_track_name()
                            )
                            p16_pen.append(
                                self.getProblem()
                                .get_parameters()
                                .presenters_conflicts_weight
                            )
        p16_list.append("Total")
        p16_pen.append(sum(p16_pen))
        p16_pen.insert(0, "")
        df34 = pd.DataFrame(p16_list)
        df35 = pd.DataFrame(p16_pen)

        # Preparing Presenters Conflicts [TS]
        p19_list = ["Evaluate Presenters Conflicts [TS]"]
        p19_pen = []
        di = {
            str(session) + str(ts): []
            for session in range(self.getProblem().get_number_of_sessions())
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (
                        (self.getSolSubmissions()[session][room][ts] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(
                                    self.getSolSubmissions()[session][room][ts]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.getSolSubmissions()[session][room][ts]
                        )
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.getProblem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.getProblem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_presenter_conflicts_list()
                            ):
                                p19_list.append(
                                    str(
                                        self.getProblem()
                                        .get_submission(di[str(session) + str(ts)][j])
                                        .get_submission_name()
                                    )
                                    + " - "
                                    + str(
                                        self.getProblem()
                                        .get_submission(di[str(session) + str(ts)][z])
                                        .get_submission_name()
                                    )
                                )
                                p19_pen.append(
                                    self.getProblem()
                                    .get_parameters()
                                    .presenters_conflicts_timeslot_level_weight
                                )
        p19_list.append("Total")
        p19_pen.append(sum(p19_pen))
        p19_pen.insert(0, "")
        df40 = pd.DataFrame(p19_list)
        df41 = pd.DataFrame(p19_pen)

        # Preparing Attendees Conflicts[TS]
        p20_list = ["Evaluate Attendees Conflicts [TS]"]
        p20_pen = []
        di = {
            str(session) + str(ts): []
            for session in range(self.getProblem().get_number_of_sessions())
            for ts in range(
                self.getProblem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.getSolTracks())):
            for room in range(len(self.getSolTracks()[session])):
                for ts in range(len(self.getSolSubmissions()[session][room])):
                    if (
                        (self.getSolSubmissions()[session][room][ts] != -1)
                        and (
                            len(
                                self.getProblem()
                                .get_submission(
                                    self.getSolSubmissions()[session][room][ts]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.getSolSubmissions()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.getSolSubmissions()[session][room][ts]
                        )
        for session in range(len(self.getSolTracks())):
            for ts in range(len(self.getSolSubmissions()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.getProblem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.getProblem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_attendee_conflicts_list()
                            ):
                                p20_list.append(
                                    self.getProblem()
                                    .get_submission(di[str(session) + str(ts)][j])
                                    .get_submission_name()
                                    + " - "
                                    + self.getProblem()
                                    .get_submission(di[str(session) + str(ts)][z])
                                    .get_submission_name()
                                )
                                p20_pen.append(
                                    self.getProblem()
                                    .get_parameters()
                                    .attendees_conflicts_timeslot_level_weight
                                )
        p20_list.append("Total")
        p20_pen.append(sum(p20_pen))
        p20_pen.insert(0, "")
        df42 = pd.DataFrame(p20_list)
        df43 = pd.DataFrame(p20_pen)

        # Writing to excel file
        with pd.ExcelWriter(file_name) as writer:
            # Sol tracks
            df.to_excel(writer, sheet_name="sol")
            # Sol submissions
            df2.to_excel(
                writer,
                sheet_name="sol",
                startrow=self.getProblem().get_number_of_sessions() + 2,
                header=False,
            )
            # Objective
            df3.to_excel(writer, sheet_name="violations", index=False, header=False)
            # Tracks|Sessions
            df4.to_excel(
                writer, sheet_name="violations", startcol=1, index=False, header=False
            )
            df5.to_excel(
                writer, sheet_name="violations", startcol=2, index=False, header=False
            )
            # Tracks|Rooms
            df6.to_excel(
                writer, sheet_name="violations", startcol=3, index=False, header=False
            )
            df7.to_excel(
                writer, sheet_name="violations", startcol=4, index=False, header=False
            )
            # Sessions|Rooms
            df8.to_excel(
                writer, sheet_name="violations", startcol=5, index=False, header=False
            )
            df9.to_excel(
                writer, sheet_name="violations", startcol=6, index=False, header=False
            )
            # Similar Tracks
            df10.to_excel(
                writer, sheet_name="violations", startcol=7, index=False, header=False
            )
            df11.to_excel(
                writer, sheet_name="violations", startcol=8, index=False, header=False
            )
            # NumberOfRoomsPerTrack
            df12.to_excel(
                writer, sheet_name="violations", startcol=9, index=False, header=False
            )
            df13.to_excel(
                writer, sheet_name="violations", startcol=10, index=False, header=False
            )
            # Parallel Tracks
            df14.to_excel(
                writer, sheet_name="violations", startcol=11, index=False, header=False
            )
            df15.to_excel(
                writer, sheet_name="violations", startcol=12, index=False, header=False
            )
            # Consecutive Tracks
            df16.to_excel(
                writer, sheet_name="violations", startcol=13, index=False, header=False
            )
            df17.to_excel(
                writer, sheet_name="violations", startcol=14, index=False, header=False
            )
            # Submissions|Timezones
            df20.to_excel(
                writer, sheet_name="violations", startcol=15, index=False, header=False
            )
            df21.to_excel(
                writer, sheet_name="violations", startcol=16, index=False, header=False
            )
            # Submissions Order
            df24.to_excel(
                writer, sheet_name="violations", startcol=17, index=False, header=False
            )
            df25.to_excel(
                writer, sheet_name="violations", startcol=18, index=False, header=False
            )
            # Submissions|Sessions
            df26.to_excel(
                writer, sheet_name="violations", startcol=19, index=False, header=False
            )
            df27.to_excel(
                writer, sheet_name="violations", startcol=20, index=False, header=False
            )
            # Submissions|Rooms
            df28.to_excel(
                writer, sheet_name="violations", startcol=21, index=False, header=False
            )
            df29.to_excel(
                writer, sheet_name="violations", startcol=22, index=False, header=False
            )
            # Presenters Conflicts [S]
            df30.to_excel(
                writer, sheet_name="violations", startcol=23, index=False, header=False
            )
            df31.to_excel(
                writer, sheet_name="violations", startcol=24, index=False, header=False
            )
            # Attendees Conflicts [S]
            df32.to_excel(
                writer, sheet_name="violations", startcol=25, index=False, header=False
            )
            df33.to_excel(
                writer, sheet_name="violations", startcol=26, index=False, header=False
            )
            # Chairs Conflicts
            df34.to_excel(
                writer, sheet_name="violations", startcol=27, index=False, header=False
            )
            df35.to_excel(
                writer, sheet_name="violations", startcol=28, index=False, header=False
            )
            # Presenters Conflicts [TS]
            df40.to_excel(
                writer, sheet_name="violations", startcol=29, index=False, header=False
            )
            df41.to_excel(
                writer, sheet_name="violations", startcol=30, index=False, header=False
            )
            # Attendees Conflicts [TS]
            df42.to_excel(
                writer, sheet_name="violations", startcol=31, index=False, header=False
            )
            df43.to_excel(
                writer, sheet_name="violations", startcol=32, index=False, header=False
            )

    def ReadSolution(self, file_name=None):
        # Creating temporary tracks solution
        file = pd.read_excel(
            file_name, header=None, keep_default_na=False, na_filter=False
        )
        temp2 = []
        for session in range(1, self.getProblem().get_number_of_sessions() + 1):
            temp = []
            for room in range(1, len(file.keys())):
                if file.iloc[session][room] != "":
                    temp.append(
                        self.getProblem().get_track_index(file.iloc[session][room])
                    )
                else:
                    temp.append(-1)
            temp2.append(temp)

        # Converting temporary tracks solution into permanent tracks solution
        for session in range(len(temp2)):
            for room in range(len(temp2[session])):
                self.getSolTracks()[session][room] = temp2[session][room]

        # Creating temporary submissions solution
        temp3 = []
        sum_ts = 0
        for session in range(self.getProblem().get_number_of_sessions()):
            index = self.getProblem().get_number_of_sessions() + 1 + sum_ts
            temp2 = []
            for room in range(1, len(file.keys())):
                temp = []
                for ts in range(
                    self.getProblem().get_session(session).get_session_max_time_slots()
                ):
                    index += 1
                    if file.iloc[index][room] != "":
                        temp.append(
                            self.getProblem().get_submission_index(
                                file.iloc[index][room]
                            )
                        )
                    else:
                        temp.append(-1)
                index = self.getProblem().get_number_of_sessions() + 1 + sum_ts
                temp2.append(temp)
            temp3.append(temp2)
            sum_ts += (
                self.getProblem().get_session(session).get_session_max_time_slots()
            )

        # Converting temporary submissions solution into permanent submissions solution
        for session in range(len(temp3)):
            for room in range(len(temp3[session])):
                for ts in range(
                    self.getProblem().get_session(session).get_session_max_time_slots()
                ):
                    self.getSolSubmissions()[session][room][ts] = temp3[session][room][
                        ts
                    ]


class InitialSolution(Solution):
    def __init__(self, problem):
        Solution.__init__(self, problem)


class RandomInd(InitialSolution):
    def __init__(self, problem):
        InitialSolution.__init__(self, problem)
        temp = [
            sub
            for sub in range(self.getProblem().get_number_of_submissions())
            if self.getProblem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            > 1
        ]
        temp2 = [
            sub
            for sub in range(self.getProblem().get_number_of_submissions())
            if self.getProblem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            == 1
        ]
        sessions = [
            session for session in range(self.getProblem().get_number_of_sessions())
        ]
        rooms = [room for room in range(self.getProblem().get_number_of_rooms())]
        np.random.shuffle(sessions)
        np.random.shuffle(rooms)
        while True:
            np.random.shuffle(temp)
            for sub in temp:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if (
                            (
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                                <= self.getSolSubmissions()[session][room].count(-1)
                            )
                            and (
                                self.getProblem().get_track_index(
                                    self.getProblem()
                                    .get_submission(sub)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                                == self.getSolTracks()[session][room]
                            )
                        ) or (
                            (
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                                <= self.getSolSubmissions()[session][room].count(-1)
                            )
                            and (self.getSolTracks()[session][room] == -1)
                        ):
                            for ts in range(
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                            ):
                                i = self.getSolSubmissions()[session][room].index(-1)
                                self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = (
                                self.getProblem().get_track_index(
                                    self.getProblem()
                                    .get_submission(sub)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                            )
            np.random.shuffle(sessions)
            np.random.shuffle(rooms)
            np.random.shuffle(temp2)
            for sub in temp2:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if (
                            (
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                                <= self.getSolSubmissions()[session][room].count(-1)
                            )
                            and (
                                self.getProblem().get_track_index(
                                    self.getProblem()
                                    .get_submission(sub)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                                == self.getSolTracks()[session][room]
                            )
                        ) or (
                            (
                                self.getProblem()
                                .get_submission(sub)
                                .get_submission_required_time_slots()
                                <= self.getSolSubmissions()[session][room].count(-1)
                            )
                            and (self.getSolTracks()[session][room] == -1)
                        ):
                            i = self.getSolSubmissions()[session][room].index(-1)
                            self.getSolSubmissions()[session][room][i] = sub
                            stop = True
                            self.getSolTracks()[session][room] = (
                                self.getProblem().get_track_index(
                                    self.getProblem()
                                    .get_submission(sub)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                            )

            if self.EvaluateAllSubmissionsScheduled() == True:
                # Creating Ind sol
                temp3 = [[] for i in range(self.getProblem().get_number_of_tracks())]
                for i in range(len(self.getSolTracks())):
                    for j in range(len(self.getSolTracks()[i])):
                        if self.getSolTracks()[i][j] != -1:
                            for x in range(len(self.getSolSubmissions()[i][j])):
                                if (self.getSolSubmissions()[i][j][x] != -1) and (
                                    self.getSolSubmissions()[i][j][x]
                                    not in temp3[self.getSolTracks()[i][j]]
                                ):
                                    temp3[self.getSolTracks()[i][j]].append(
                                        self.getSolSubmissions()[i][j][x]
                                    )
                self.setIndSolSubmissions(temp3)
                for session in range(self.getProblem().get_number_of_sessions()):
                    for room in range(self.getProblem().get_number_of_rooms()):
                        if self.getSolSubmissions()[session][room].count(-1) == len(
                            self.getSolSubmissions()[session][room]
                        ):
                            self.getSolTracks()[session][room] = -1
                self.resetSolSubmissions()
                self.convertSol()
                if self.EvaluateAllSubmissionsScheduled() == True:
                    return
                else:
                    self.resetSolTracks()
                    self.resetSolSubmissions()
                    self.resetIndSolSubmissions()
            else:
                self.resetSolTracks()
                self.resetSolSubmissions()
                self.resetIndSolSubmissions()

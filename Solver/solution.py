# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.problem import Problem
from pathlib import Path
from typing import List, Callable
import config
import numpy as np
import pandas as pd
import logging


class Solution:
    def __init__(self, problem: Problem):
        self.__problem: Problem = problem
        self.__tracks_solution: List[List[int]] = [
            [-1 for room in range(self.get_problem().get_number_of_rooms())]
            for session in range(self.get_problem().get_number_of_sessions())
        ]
        self.__submissions_solution: List[List[List[int]]] = [
            [
                [
                    -1
                    for time_slot in range(
                        self.get_problem()
                        .get_session(session)
                        .get_session_max_time_slots()
                    )
                ]
                for room in range(self.get_problem().get_number_of_rooms())
            ]
            for session in range(self.get_problem().get_number_of_sessions())
        ]
        self.__submissions_indirect_solution: List[List[int]] = [
            [
                self.get_problem().get_submission_index(
                    submission.get_submission_name()
                )
                for submission in self.get_problem()
                .get_track(track)
                .get_track_submissions_list()
            ]
            for track in range(self.get_problem().get_number_of_tracks())
        ]
        self.__generate_valuations()

    def get_problem(self) -> Problem:
        return self.__problem

    def get_tracks_solution(self) -> List[List[int]]:
        return self.__tracks_solution

    def get_submissions_solution(self) -> List[List[List[int]]]:
        return self.__submissions_solution

    def get_submissions_indirect_solution(self) -> List[List[int]]:
        return self.__submissions_indirect_solution

    def set_submissions_indirect_solution(
        self, submissions_indirect_solution: List[List[int]]
    ) -> None:
        self.__submissions_indirect_solution = submissions_indirect_solution

    def set_best_solution(
        self,
        tracks_solution: List[List[int]],
        submissions_solution: List[List[List[int]]],
    ) -> None:
        self.__tracks_solution = tracks_solution
        self.__submissions_solution = submissions_solution

    def restore_solution(
        self,
        tracks_solution: List[List[int]],
        submissions_solution: List[List[List[int]]],
        submissions_indirect_solution: List[List[int]],
    ) -> None:
        self.__tracks_solution = tracks_solution
        self.__submissions_solution = submissions_solution
        self.__submissions_indirect_solution = submissions_indirect_solution

    def reset_tracks_solution(self) -> None:
        self.__tracks_solution = [
            [-1 for room in range(self.get_problem().get_number_of_rooms())]
            for session in range(self.get_problem().get_number_of_sessions())
        ]

    def reset_submissions_solution(self) -> None:
        self.__submissions_solution = [
            [
                [
                    -1
                    for time_slot in range(
                        self.get_problem()
                        .get_session(session)
                        .get_session_max_time_slots()
                    )
                ]
                for room in range(self.get_problem().get_number_of_rooms())
            ]
            for session in range(self.get_problem().get_number_of_sessions())
        ]

    def reset_submissions_indirect_solution(self) -> None:
        self.__submissions_indirect_solution = [
            [
                self.get_problem().get_submission_index(
                    submission.get_submission_name()
                )
                for submission in self.get_problem()
                .get_track(track)
                .get_track_submissions_list()
            ]
            for track in range(self.get_problem().get_number_of_tracks())
        ]

    def __generate_valuations(self) -> None:
        self.__evaluations = []
        self.__evaluations_names = {}
        if self.get_problem().get_parameters().tracks_sessions_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().tracks_sessions_penalty_weight
                    * self.evaluate_tracks_sessions()
                ),
                "Tracks_Sessions|Penalty:",
            )
        if self.get_problem().get_parameters().tracks_rooms_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().tracks_rooms_penalty_weight
                    * self.evaluate_tracks_rooms()
                ),
                "Tracks_Rooms|Penalty:",
            )
        if self.get_problem().get_parameters().sessions_rooms_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().sessions_rooms_penalty_weight
                    * self.evaluate_sessions_rooms()
                ),
                "Sessions_Rooms|Penalty",
            )
        if self.get_problem().get_parameters().similar_tracks_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().similar_tracks_penalty_weight
                    * self.evaluate_similar_tracks()
                ),
                "Similar Tracks:",
            )
        if self.get_problem().get_parameters().num_rooms_per_track_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().num_rooms_per_track_weight
                    * self.evaluate_number_of_rooms_per_track()
                ),
                "Number of rooms per track:",
            )
        if self.get_problem().get_parameters().parallel_tracks_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().parallel_tracks_weight
                    * self.evaluate_parallel_tracks()
                ),
                "Parallel tracks:",
            )
        if self.get_problem().get_parameters().consecutive_tracks_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().consecutive_tracks_weight
                    * self.evaluate_consecutive_tracks()
                ),
                "Consecutive tracks:",
            )
        if self.get_problem().get_parameters().submissions_timezones_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem()
                    .get_parameters()
                    .submissions_timezones_penalty_weight
                    * self.evaluate_submissions_timezones()
                ),
                "Submissions timezones:",
            )
        if self.get_problem().get_parameters().submissions_order_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().submissions_order_weight
                    * self.evaluate_submissions_order()
                ),
                "Submissions order:",
            )
        if self.get_problem().get_parameters().submissions_sessions_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem()
                    .get_parameters()
                    .submissions_sessions_penalty_weight
                    * self.evaluate_submissions_sessions()
                ),
                "Submissions_Sessions|Penalty:",
            )
        if self.get_problem().get_parameters().submissions_rooms_penalty_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().submissions_rooms_penalty_weight
                    * self.evaluate_submissions_rooms()
                ),
                "Submissions_Rooms|Penalty:",
            )
        if self.get_problem().get_parameters().presenters_conflicts_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().presenters_conflicts_weight
                    * self.evaluate_presenters_conflicts_session_level()
                ),
                "Presenters conflicts [Session Level]:",
            )
        if self.get_problem().get_parameters().attendees_conflicts_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().attendees_conflicts_weight
                    * self.evaluate_attendees_conflicts_session_level()
                ),
                "Attendees conflicts [Session Level]:",
            )
        if self.get_problem().get_parameters().chairs_conflicts_weight > 0:
            self.__set_evaluation(
                lambda: (
                    self.get_problem().get_parameters().chairs_conflicts_weight
                    * self.evaluate_track_chairs_conflicts()
                ),
                "Chairs conflicts:",
            )
        if (
            self.get_problem()
            .get_parameters()
            .presenters_conflicts_timeslot_level_weight
            > 0
        ):
            self.__set_evaluation(
                lambda: (
                    self.get_problem()
                    .get_parameters()
                    .presenters_conflicts_timeslot_level_weight
                    * self.evaluate_presenters_conflicts_time_slot_level()
                ),
                "Presenters conflicts [Timeslot Level]:",
            )
        if (
            self.get_problem()
            .get_parameters()
            .attendees_conflicts_timeslot_level_weight
            > 0
        ):
            self.__set_evaluation(
                lambda: (
                    self.get_problem()
                    .get_parameters()
                    .attendees_conflicts_timeslot_level_weight
                    * self.evaluate_attendees_conflicts_time_slot_level()
                ),
                "Attendees conflicts [Timeslot Level]:",
            )
        self.__set_evaluation(
            lambda: self.evaluate_multi_slot_submissions(),
            "Submissions with multiple timeslots in different sessions:",
        )

    def __set_evaluation(
        self, evaluation_function: Callable[[], int], evaluation_name: str
    ) -> None:
        self.__evaluations.append(evaluation_function)
        self.__evaluations_names[evaluation_function] = evaluation_name

    def get_evaluations_list(self) -> List[Callable[[], int]]:
        return self.__evaluations

    def get_evaluation_name(self, evaluation_function: Callable[[], int]) -> str:
        return self.__evaluations_names[evaluation_function]

    def evaluate_tracks_sessions(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    value += self.get_problem().get_tracks_sessions_penalty_by_index(
                        self.get_tracks_solution()[session][room], session
                    )
        return value

    def evaluate_tracks_rooms(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    value += self.get_problem().get_tracks_rooms_penalty_by_index(
                        self.get_tracks_solution()[session][room], room
                    )
        return value

    def evaluate_sessions_rooms(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    value += self.get_problem().get_sessions_rooms_penalty_by_index(
                        session, room
                    )
        return value

    def evaluate_similar_tracks(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for this_room in range(len(self.get_tracks_solution()[session])):
                for other_room in range(
                    this_room, len(self.get_tracks_solution()[session])
                ):
                    if (
                        (
                            self.get_tracks_solution()[session][this_room]
                            != self.get_tracks_solution()[session][other_room]
                        )
                        and (self.get_tracks_solution()[session][this_room] != -1)
                        and (self.get_tracks_solution()[session][other_room] != -1)
                    ):
                        value += self.get_problem().get_tracks_tracks_penalty_by_index(
                            self.get_tracks_solution()[session][this_room],
                            self.get_tracks_solution()[session][other_room],
                        )
        return value

    def evaluate_number_of_rooms_per_track(self) -> int:
        value = 0
        rooms_per_track_map = {
            track: [] for track in range(self.get_problem().get_number_of_tracks())
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if (self.get_tracks_solution()[session][room] != -1) and (
                    room
                    not in rooms_per_track_map[
                        self.get_tracks_solution()[session][room]
                    ]
                ):
                    rooms_per_track_map[
                        self.get_tracks_solution()[session][room]
                    ].append(room)

        for rooms in rooms_per_track_map.values():
            if len(rooms) > 1:
                value += len(rooms) - 1
        return value

    def evaluate_parallel_tracks(self) -> int:
        value = 0
        sessions = [
            tuple(self.get_tracks_solution()[session])
            for session in range(len(self.get_tracks_solution()))
        ]

        for track in range(self.get_problem().get_number_of_tracks()):
            for session in sessions:
                tracks_count = session.count(track)
                if tracks_count > 1:
                    value += tracks_count - 1
        return value

    def evaluate_consecutive_tracks(self) -> int:
        value = 0
        sessions_per_track_map = {
            track: [] for track in range(self.get_problem().get_number_of_tracks())
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if (self.get_tracks_solution()[session][room] != -1) and (
                    session
                    not in sessions_per_track_map[
                        self.get_tracks_solution()[session][room]
                    ]
                ):
                    sessions_per_track_map[
                        self.get_tracks_solution()[session][room]
                    ].append(session)

        for sessions in sessions_per_track_map.values():
            if (len(sessions) > 1) and (
                sum(sessions)
                != sum(range(sessions[0], sessions[len(sessions) - 1] + 1))
            ):
                value += 1
        return value

    def evaluate_submissions_timezones(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if self.get_submissions_solution()[session][room][time_slot] != -1:
                        value += self.get_problem().get_submissions_timezones_penalty_by_index(
                            self.get_submissions_solution()[session][room][time_slot],
                            session,
                        )
        return value

    def evaluate_submissions_order(self) -> int:
        value = 0
        submissions_per_track_map = {
            track: [] for track in range(self.get_problem().get_number_of_tracks())
        }
        submissions_per_time_slot_map = {
            self.get_problem().get_session(session).get_session_name()
            + str(time_slot): []
            for session in range(len(self.get_tracks_solution()))
            for time_slot in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    for time_slot in range(
                        len(self.get_submissions_solution()[session][room])
                    ):
                        if (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        ) and (
                            self.get_submissions_solution()[session][room][time_slot]
                            not in submissions_per_track_map[
                                self.get_tracks_solution()[session][room]
                            ]
                        ):
                            submissions_per_track_map[
                                self.get_tracks_solution()[session][room]
                            ].append(
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ]
                            )
                        if (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        ) and (
                            self.get_submissions_solution()[session][room][time_slot]
                            not in submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ]
                        ):
                            submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ].append(
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ]
                            )

        for time_slot in submissions_per_time_slot_map.values():
            for this_sub in range(len(time_slot) - 1):
                for other_sub in range(this_sub + 1, len(time_slot)):
                    if (
                        self.get_problem()
                        .get_submission(time_slot[this_sub])
                        .get_submission_track()
                        .get_track_name()
                        == self.get_problem()
                        .get_submission(time_slot[other_sub])
                        .get_submission_track()
                        .get_track_name()
                    ) and (
                        (
                            self.get_problem()
                            .get_submission(time_slot[this_sub])
                            .get_submission_order()
                            != 0
                        )
                        and (
                            self.get_problem()
                            .get_submission(time_slot[other_sub])
                            .get_submission_order()
                            != 0
                        )
                    ):
                        value += 1

        for track in range(self.get_problem().get_number_of_tracks()):
            order = 1
            for submission in submissions_per_track_map[track]:
                if (
                    self.get_problem().get_submission(submission).get_submission_order()
                    != order
                ) and (
                    self.get_problem().get_submission(submission).get_submission_order()
                    != 0
                ):
                    value += 1
                order += 1
        return value

    def evaluate_submissions_sessions(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if self.get_submissions_solution()[session][room][time_slot] != -1:
                        value += self.get_problem().get_submissions_sessions_penalty_by_index(
                            self.get_submissions_solution()[session][room][time_slot],
                            session,
                        )
        return value

    def evaluate_submissions_rooms(self) -> int:
        value = 0
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if self.get_submissions_solution()[session][room][time_slot] != -1:
                        value += (
                            self.get_problem().get_submissions_rooms_penalty_by_index(
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ],
                                room,
                            )
                        )
        return value

    def evaluate_presenters_conflicts_session_level(self) -> int:
        value = 0
        submission_room_pairs_per_session_map = {
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if (
                        (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        )
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            (
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ],
                                room,
                            )
                            not in submission_room_pairs_per_session_map[session]
                        )
                    ):
                        submission_room_pairs_per_session_map[session].append(
                            (
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ],
                                room,
                            )
                        )

        for session in range(len(self.get_tracks_solution())):
            if len(submission_room_pairs_per_session_map[session]) > 1:
                for this_submission_room_pair in range(
                    len(submission_room_pairs_per_session_map[session]) - 1
                ):
                    for other_submission_room_pair in range(
                        this_submission_room_pair + 1,
                        len(submission_room_pairs_per_session_map[session]),
                    ):
                        if (
                            self.get_problem().get_submission(
                                submission_room_pairs_per_session_map[session][
                                    this_submission_room_pair
                                ][0]
                            )
                            in self.get_problem()
                            .get_submission(
                                submission_room_pairs_per_session_map[session][
                                    other_submission_room_pair
                                ][0]
                            )
                            .get_submission_presenter_conflicts_list()
                        ) and (
                            submission_room_pairs_per_session_map[session][
                                this_submission_room_pair
                            ][1]
                            != submission_room_pairs_per_session_map[session][
                                other_submission_room_pair
                            ][1]
                        ):
                            value += 1
        return value

    def evaluate_attendees_conflicts_session_level(self) -> int:
        value = 0
        submission_room_pairs_per_session_map = {
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if (
                        (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        )
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            (
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ],
                                room,
                            )
                            not in submission_room_pairs_per_session_map[session]
                        )
                    ):
                        submission_room_pairs_per_session_map[session].append(
                            (
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ],
                                room,
                            )
                        )

        for session in range(len(self.get_tracks_solution())):
            if len(submission_room_pairs_per_session_map[session]) > 1:
                for this_submission_room_pair in range(
                    len(submission_room_pairs_per_session_map[session]) - 1
                ):
                    for other_submission_room_pair in range(
                        this_submission_room_pair + 1,
                        len(submission_room_pairs_per_session_map[session]),
                    ):
                        if (
                            self.get_problem().get_submission(
                                submission_room_pairs_per_session_map[session][
                                    this_submission_room_pair
                                ][0]
                            )
                            in self.get_problem()
                            .get_submission(
                                submission_room_pairs_per_session_map[session][
                                    other_submission_room_pair
                                ][0]
                            )
                            .get_submission_attendee_conflicts_list()
                        ) and (
                            submission_room_pairs_per_session_map[session][
                                this_submission_room_pair
                            ][1]
                            != submission_room_pairs_per_session_map[session][
                                other_submission_room_pair
                            ][1]
                        ):
                            value += 1
        return value

    def evaluate_track_chairs_conflicts(self) -> int:
        value = 0
        tracks_per_session_map = {
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if (self.get_tracks_solution()[session][room] != -1) and (
                    len(
                        self.get_problem()
                        .get_track(self.get_tracks_solution()[session][room])
                        .get_track_chair_conflicts_list()
                    )
                    != 0
                ):
                    tracks_per_session_map[session].append(
                        self.get_tracks_solution()[session][room]
                    )

        for session in range(len(self.get_tracks_solution())):
            if len(tracks_per_session_map[session]) > 1:
                for this_track in range(len(tracks_per_session_map[session]) - 1):
                    for other_track in range(
                        this_track + 1, len(tracks_per_session_map[session])
                    ):
                        if (
                            self.get_problem().get_track(
                                tracks_per_session_map[session][this_track]
                            )
                            in self.get_problem()
                            .get_track(tracks_per_session_map[session][other_track])
                            .get_track_chair_conflicts_list()
                        ):
                            value += 1
        return value

    def evaluate_presenters_conflicts_time_slot_level(self) -> int:
        value = 0
        submissions_per_time_slot_map = {
            self.get_problem().get_session(session).get_session_name()
            + str(time_slot): []
            for session in range(self.get_problem().get_number_of_sessions())
            for time_slot in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if (
                        (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        )
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.get_submissions_solution()[session][room][time_slot]
                            not in submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ]
                        )
                    ):
                        submissions_per_time_slot_map[
                            self.get_problem().get_session(session).get_session_name()
                            + str(time_slot)
                        ].append(
                            self.get_submissions_solution()[session][room][time_slot]
                        )

        for session in range(len(self.get_tracks_solution())):
            for time_slot in range(len(self.get_submissions_solution()[session][room])):
                if (
                    len(
                        submissions_per_time_slot_map[
                            self.get_problem().get_session(session).get_session_name()
                            + str(time_slot)
                        ]
                    )
                    > 1
                ):
                    for this_submission in range(
                        len(
                            submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ]
                        )
                        - 1
                    ):
                        for other_submission in range(
                            this_submission + 1,
                            len(
                                submissions_per_time_slot_map[
                                    self.get_problem()
                                    .get_session(session)
                                    .get_session_name()
                                    + str(time_slot)
                                ]
                            ),
                        ):
                            if (
                                self.get_problem().get_submission(
                                    submissions_per_time_slot_map[
                                        self.get_problem()
                                        .get_session(session)
                                        .get_session_name()
                                        + str(time_slot)
                                    ][this_submission]
                                )
                                in self.get_problem()
                                .get_submission(
                                    submissions_per_time_slot_map[
                                        self.get_problem()
                                        .get_session(session)
                                        .get_session_name()
                                        + str(time_slot)
                                    ][other_submission]
                                )
                                .get_submission_presenter_conflicts_list()
                            ):
                                value += 1
        return value

    def evaluate_attendees_conflicts_time_slot_level(self) -> int:
        value = 0
        submissions_per_time_slot_map = {
            self.get_problem().get_session(session).get_session_name()
            + str(time_slot): []
            for session in range(self.get_problem().get_number_of_sessions())
            for time_slot in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if (
                        (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        )
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.get_submissions_solution()[session][room][time_slot]
                            not in submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ]
                        )
                    ):
                        submissions_per_time_slot_map[
                            self.get_problem().get_session(session).get_session_name()
                            + str(time_slot)
                        ].append(
                            self.get_submissions_solution()[session][room][time_slot]
                        )
        for session in range(len(self.get_tracks_solution())):
            for time_slot in range(len(self.get_submissions_solution()[session][room])):
                if (
                    len(
                        submissions_per_time_slot_map[
                            self.get_problem().get_session(session).get_session_name()
                            + str(time_slot)
                        ]
                    )
                    > 1
                ):
                    for this_submission in range(
                        len(
                            submissions_per_time_slot_map[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(time_slot)
                            ]
                        )
                        - 1
                    ):
                        for other_submission in range(
                            this_submission + 1,
                            len(
                                submissions_per_time_slot_map[
                                    self.get_problem()
                                    .get_session(session)
                                    .get_session_name()
                                    + str(time_slot)
                                ]
                            ),
                        ):
                            if (
                                self.get_problem().get_submission(
                                    submissions_per_time_slot_map[
                                        self.get_problem()
                                        .get_session(session)
                                        .get_session_name()
                                        + str(time_slot)
                                    ][this_submission]
                                )
                                in self.get_problem()
                                .get_submission(
                                    submissions_per_time_slot_map[
                                        self.get_problem()
                                        .get_session(session)
                                        .get_session_name()
                                        + str(time_slot)
                                    ][other_submission]
                                )
                                .get_submission_attendee_conflicts_list()
                            ):
                                value += 1
        return value

    def evaluate_multi_slot_submissions(self) -> int:
        value = 0
        multi_slot_submissions_per_session_room_pair_map = {
            self.get_problem().get_session(session).get_session_name()
            + self.get_problem().get_room(room).get_room_name(): []
            for session in range(self.get_problem().get_number_of_sessions())
            for room in range(self.get_problem().get_number_of_rooms())
        }
        time_slots_per_submission_map = {
            sub: []
            for sub in range(self.get_problem().get_number_of_submissions())
            if self.get_problem()
            .get_submission(sub)
            .get_submission_required_time_slots()
            > 1
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if (
                        self.get_submissions_solution()[session][room][time_slot] != -1
                    ) and (
                        self.get_problem()
                        .get_submission(
                            self.get_submissions_solution()[session][room][time_slot]
                        )
                        .get_submission_required_time_slots()
                        > 1
                    ):
                        multi_slot_submissions_per_session_room_pair_map[
                            self.get_problem().get_session(session).get_session_name()
                            + self.get_problem().get_room(room).get_room_name()
                        ].append(
                            self.get_submissions_solution()[session][room][time_slot]
                        )
                        time_slots_per_submission_map[
                            self.get_submissions_solution()[session][room][time_slot]
                        ].append(time_slot)

        for (
            multi_slot_submissions
        ) in multi_slot_submissions_per_session_room_pair_map.values():
            if len(multi_slot_submissions) != 0:
                temp = set(multi_slot_submissions)
                for multi_slot_submission in temp:
                    if (
                        self.get_problem()
                        .get_submission(multi_slot_submission)
                        .get_submission_required_time_slots()
                        != multi_slot_submissions.count(multi_slot_submission)
                    ):
                        value += 10000000

        for time_slots in time_slots_per_submission_map.values():
            if len(time_slots) == 0:
                return 1000000000
            if sum(range(time_slots[0], time_slots[len(time_slots) - 1] + 1)) != sum(
                time_slots
            ):
                value += 1000000000
        return value

    def evaluate_all_submissions_scheduled(self) -> bool:
        scheduled_submissions = [
            self.get_submissions_solution()[session][room][time_slot]
            for session in range(len(self.get_tracks_solution()))
            for room in range(len(self.get_tracks_solution()[session]))
            for time_slot in range(len(self.get_submissions_solution()[session][room]))
            if self.get_submissions_solution()[session][room][time_slot] != -1
        ]
        for submission in range(self.get_problem().get_number_of_submissions()):
            if (submission not in scheduled_submissions) or (
                self.get_problem()
                .get_submission(submission)
                .get_submission_required_time_slots()
                != scheduled_submissions.count(submission)
            ):
                return False
        return True

    def validate_solution(self) -> bool:
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    if self.get_tracks_solution()[session][room] != -1:
                        if (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        ):
                            if (
                                self.get_problem().get_submission(
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                )
                                not in self.get_problem()
                                .get_track(self.get_tracks_solution()[session][room])
                                .get_track_submissions_list()
                            ):
                                return False
        return True

    def evaluate_solution(self) -> int:
        return sum([evaluation() for evaluation in self.get_evaluations_list()])

    def evaluate_solution_fast(self, previous_objective: int) -> int:
        current_objective = 0
        for evaluation in self.get_evaluations_list():
            current_objective += evaluation()
            if current_objective > previous_objective:
                return current_objective
        return current_objective

    def copy_whole_solution(self) -> List:
        copy_tracks_solution = []
        copy_submissions_solution = []
        for session in range(len(self.get_tracks_solution())):
            temp = []
            temp3 = []
            for room in range(len(self.get_tracks_solution()[session])):
                temp.append(self.get_tracks_solution()[session][room])
                temp2 = []
                for time_slot in range(
                    len(self.get_submissions_solution()[session][room])
                ):
                    temp2.append(
                        self.get_submissions_solution()[session][room][time_slot]
                    )
                temp3.append(temp2)
            copy_tracks_solution.append(temp)
            copy_submissions_solution.append(temp3)
        copy_submissions_indirect_solution = []
        for track in range(len(self.get_submissions_indirect_solution())):
            temp = []
            for submission in range(
                len(self.get_submissions_indirect_solution()[track])
            ):
                temp.append(self.get_submissions_indirect_solution()[track][submission])
            copy_submissions_indirect_solution.append(temp)
        return (
            copy_tracks_solution,
            copy_submissions_solution,
            copy_submissions_indirect_solution,
        )

    def convert_indirect_solution_first_time(self) -> None:
        all_submissions = [
            self.get_submissions_indirect_solution()[track][submission]
            for track in range(len(self.get_submissions_indirect_solution()))
            for submission in range(
                len(self.get_submissions_indirect_solution()[track])
            )
        ]
        for submission in all_submissions:
            if (
                self.get_problem()
                .get_submission(submission)
                .get_submission_required_time_slots()
                == 1
            ):
                stop = False
                for session in range(self.get_problem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.get_problem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.get_problem()
                            .get_submission(submission)
                            .get_submission_required_time_slots()
                            <= self.get_submissions_solution()[session][room].count(-1)
                        ) and (
                            self.get_problem().get_track_index(
                                self.get_problem()
                                .get_submission(submission)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.get_tracks_solution()[session][room]
                        ):
                            available_time_slot = self.get_submissions_solution()[
                                session
                            ][room].index(-1)
                            self.get_submissions_solution()[session][room][
                                available_time_slot
                            ] = submission
                            stop = True

        for session in range(self.get_problem().get_number_of_sessions()):
            for room in range(self.get_problem().get_number_of_rooms()):
                if self.get_submissions_solution()[session][room].count(-1) == len(
                    self.get_submissions_solution()[session][room]
                ):
                    self.get_tracks_solution()[session][room] = -1

        submissions_indirect_solution = [
            [] for track in range(self.get_problem().get_number_of_tracks())
        ]
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    for time_slot in range(
                        len(self.get_submissions_solution()[session][room])
                    ):
                        if (
                            self.get_submissions_solution()[session][room][time_slot]
                            != -1
                        ) and (
                            self.get_submissions_solution()[session][room][time_slot]
                            not in submissions_indirect_solution[
                                self.get_tracks_solution()[session][room]
                            ]
                        ):
                            submissions_indirect_solution[
                                self.get_tracks_solution()[session][room]
                            ].append(
                                self.get_submissions_solution()[session][room][
                                    time_slot
                                ]
                            )
        self.set_submissions_indirect_solution(submissions_indirect_solution)

    def convert_solution(self) -> None:
        all_submissions = [
            self.get_submissions_indirect_solution()[track][submission]
            for track in range(len(self.get_submissions_indirect_solution()))
            for submission in range(
                len(self.get_submissions_indirect_solution()[track])
            )
        ]
        for submission in all_submissions:
            if (
                self.get_problem()
                .get_submission(submission)
                .get_submission_required_time_slots()
                > 1
            ):
                stop = False
                for session in range(self.get_problem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.get_problem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.get_problem()
                            .get_submission(submission)
                            .get_submission_required_time_slots()
                            <= self.get_submissions_solution()[session][room].count(-1)
                        ) and (
                            self.get_problem().get_track_index(
                                self.get_problem()
                                .get_submission(submission)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.get_tracks_solution()[session][room]
                        ):
                            for time_slot in range(
                                self.get_problem()
                                .get_submission(submission)
                                .get_submission_required_time_slots()
                            ):
                                available_time_slot = self.get_submissions_solution()[
                                    session
                                ][room].index(-1)
                                self.get_submissions_solution()[session][room][
                                    available_time_slot
                                ] = submission
                            stop = True
            else:
                stop = False
                for session in range(self.get_problem().get_number_of_sessions()):
                    if stop == True:
                        break
                    for room in range(self.get_problem().get_number_of_rooms()):
                        if stop == True:
                            break
                        if (
                            self.get_problem()
                            .get_submission(submission)
                            .get_submission_required_time_slots()
                            <= self.get_submissions_solution()[session][room].count(-1)
                        ) and (
                            self.get_problem().get_track_index(
                                self.get_problem()
                                .get_submission(submission)
                                .get_submission_track()
                                .get_track_name()
                            )
                            == self.get_tracks_solution()[session][room]
                        ):
                            available_time_slot = self.get_submissions_solution()[
                                session
                            ][room].index(-1)
                            self.get_submissions_solution()[session][room][
                                available_time_slot
                            ] = submission
                            stop = True

        for session in range(self.get_problem().get_number_of_sessions()):
            for room in range(self.get_problem().get_number_of_rooms()):
                if self.get_submissions_solution()[session][room].count(-1) == len(
                    self.get_submissions_solution()[session][room]
                ):
                    self.get_tracks_solution()[session][room] = -1

    def print_violations(self):
        logging.info("----- Violations breakdown -----")
        for evaluation in self.get_evaluations_list():
            value = evaluation()
            if value > 0:
                logging.info(f"{self.get_evaluation_name(evaluation)} {value}")
        logging.info("--------------------------------")

    def to_excel(self, file_path: Path) -> None:
        # Preparing sol tracks
        df = pd.DataFrame(
            self.get_tracks_solution(),
            index=[
                self.get_problem().get_session(s).get_session_name()
                for s in range(self.get_problem().get_number_of_sessions())
            ],
            columns=[
                self.get_problem().get_room(r).get_room_name()
                for r in range(self.get_problem().get_number_of_rooms())
            ],
        )
        df = df.map(
            lambda x: self.get_problem().get_track(x).get_track_name()
            if x != -1
            else ""
        )

        # Preparing sol submissions
        temp2 = []
        for session in range(self.get_problem().get_number_of_sessions()):
            for t in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            ):
                temp = []
                for room in range(self.get_problem().get_number_of_rooms()):
                    if self.get_submissions_solution()[session][room][t] != -1:
                        temp.append(
                            self.get_problem()
                            .get_submission(
                                self.get_submissions_solution()[session][room][t]
                            )
                            .get_submission_name()
                        )
                    else:
                        temp.append("")
                temp2.append(temp)
        df2 = pd.DataFrame(
            temp2,
            index=[
                self.get_problem().get_session(s).get_session_name()
                for s in range(self.get_problem().get_number_of_sessions())
                for t in range(
                    self.get_problem().get_session(s).get_session_max_time_slots()
                )
            ],
        )

        # Preparing objective
        obj = self.evaluate_solution()
        obj_list = ["Obj", "Final Objective = " + str(obj)]
        df3 = pd.DataFrame(obj_list)

        # Preparing Tracks|Sessions penalty
        p1_list = ["Evaluate Tracks|Sessions"]
        p1_pen = []
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if self.get_tracks_solution()[i][j] != -1:
                    if (
                        self.get_problem().get_tracks_sessions_penalty_by_index(
                            self.get_tracks_solution()[i][j], i
                        )
                        != 0
                    ):
                        p1_list.append(
                            self.get_problem()
                            .get_track(self.get_tracks_solution()[i][j])
                            .get_track_name()
                            + " - "
                            + self.get_problem().get_session(i).get_session_name()
                        )
                        p1_pen.append(
                            self.get_problem()
                            .get_parameters()
                            .tracks_sessions_penalty_weight
                            * self.get_problem().get_tracks_sessions_penalty_by_index(
                                self.get_tracks_solution()[i][j], i
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
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if self.get_tracks_solution()[i][j] != -1:
                    if (
                        self.get_problem().get_tracks_rooms_penalty_by_index(
                            self.get_tracks_solution()[i][j], j
                        )
                        != 0
                    ):
                        p2_list.append(
                            self.get_problem()
                            .get_track(self.get_tracks_solution()[i][j])
                            .get_track_name()
                            + " - "
                            + self.get_problem().get_room(j).get_room_name()
                        )
                        p2_pen.append(
                            self.get_problem()
                            .get_parameters()
                            .tracks_rooms_penalty_weight
                            * self.get_problem().get_tracks_rooms_penalty_by_index(
                                self.get_tracks_solution()[i][j], j
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
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if self.get_tracks_solution()[i][j] != -1:
                    if (
                        self.get_problem().get_sessions_rooms_penalty_by_index(i, j)
                        != 0
                    ):
                        p3_list.append(
                            self.get_problem().get_session(i).get_session_name()
                            + " - "
                            + self.get_problem().get_room(j).get_room_name()
                        )
                        p3_pen.append(
                            self.get_problem()
                            .get_parameters()
                            .sessions_rooms_penalty_weight
                            * self.get_problem().get_sessions_rooms_penalty_by_index(
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
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(j, len(self.get_tracks_solution()[i])):
                    if (
                        (
                            self.get_tracks_solution()[i][j]
                            != self.get_tracks_solution()[i][x]
                        )
                        and (self.get_tracks_solution()[i][j] != -1)
                        and (self.get_tracks_solution()[i][x] != -1)
                    ):
                        if (
                            self.get_problem().get_tracks_tracks_penalty_by_index(
                                self.get_tracks_solution()[i][j],
                                self.get_tracks_solution()[i][x],
                            )
                            != 0
                        ):
                            p4_list.append(
                                self.get_problem()
                                .get_track(self.get_tracks_solution()[i][j])
                                .get_track_name()
                                + " - "
                                + self.get_problem()
                                .get_track(self.get_tracks_solution()[i][x])
                                .get_track_name()
                                + " - "
                                + self.get_problem().get_session(i).get_session_name()
                            )
                            p4_pen.append(
                                self.get_problem()
                                .get_parameters()
                                .similar_tracks_penalty_weight
                                * self.get_problem().get_tracks_tracks_penalty_by_index(
                                    self.get_tracks_solution()[i][j],
                                    self.get_tracks_solution()[i][x],
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
        di = {track: [] for track in range(self.get_problem().get_number_of_tracks())}
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if (self.get_tracks_solution()[i][j] != -1) and (
                    j not in di[self.get_tracks_solution()[i][j]]
                ):
                    di[self.get_tracks_solution()[i][j]].append(j)
        t = -1
        for i in di.values():
            t += 1
            if len(i) > 1:
                p5_list.append(self.get_problem().get_track(t).get_track_name())
                p5_pen.append(
                    self.get_problem().get_parameters().num_rooms_per_track_weight
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
            tuple(self.get_tracks_solution()[session])
            for session in range(len(self.get_tracks_solution()))
        ]
        for track in range(self.get_problem().get_number_of_tracks()):
            for session in range(len(temp)):
                c = temp[session].count(track)
                if c > 1:
                    p6_list.append(
                        self.get_problem().get_track(track).get_track_name()
                        + " - "
                        + self.get_problem().get_session(session).get_session_name()
                    )
                    p6_pen.append(
                        self.get_problem().get_parameters().parallel_tracks_weight
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
        di = {track: [] for track in range(self.get_problem().get_number_of_tracks())}
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if (self.get_tracks_solution()[i][j] != -1) and (
                    i not in di[self.get_tracks_solution()[i][j]]
                ):
                    di[self.get_tracks_solution()[i][j]].append(i)
        t = -1
        for i in di.values():
            t += 1
            if (len(i) > 1) and (sum(i) != sum(range(i[0], i[len(i) - 1] + 1))):
                p7_list.append(self.get_problem().get_track(t).get_track_name())
                p7_pen.append(
                    self.get_problem().get_parameters().consecutive_tracks_weight
                )
        p7_list.append("Total")
        p7_pen.append(sum(p7_pen))
        p7_pen.insert(0, "")
        df16 = pd.DataFrame(p7_list)
        df17 = pd.DataFrame(p7_pen)

        # Preparing Submissions|Timezones penalty
        p9_list = ["Evaluate Submissions|Timezones"]
        p9_pen = []
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(len(self.get_submissions_solution()[i][j])):
                    if self.get_submissions_solution()[i][j][x] != -1:
                        if (
                            self.get_problem().get_submissions_timezones_penalty_by_index(
                                self.get_submissions_solution()[i][j][x], i
                            )
                            != 0
                        ):
                            p9_list.append(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[i][j][x]
                                )
                                .get_submission_name()
                                + " - "
                                + self.get_problem().get_session(i).get_session_name()
                            )
                            p9_pen.append(
                                self.get_problem()
                                .get_parameters()
                                .submissions_timezones_penalty_weight
                                * self.get_problem().get_submissions_timezones_penalty_by_index(
                                    self.get_submissions_solution()[i][j][x], i
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
        di = {track: [] for track in range(self.get_problem().get_number_of_tracks())}
        session_ts = {
            self.get_problem().get_session(session).get_session_name() + str(ts): []
            for session in range(len(self.get_tracks_solution()))
            for ts in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }

        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                if self.get_tracks_solution()[session][room] != -1:
                    for ts in range(
                        len(self.get_submissions_solution()[session][room])
                    ):
                        if (
                            self.get_submissions_solution()[session][room][ts] != -1
                        ) and (
                            self.get_submissions_solution()[session][room][ts]
                            not in di[self.get_tracks_solution()[session][room]]
                        ):
                            di[self.get_tracks_solution()[session][room]].append(
                                self.get_submissions_solution()[session][room][ts]
                            )
                        if (
                            self.get_submissions_solution()[session][room][ts] != -1
                        ) and (
                            self.get_submissions_solution()[session][room][ts]
                            not in session_ts[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ]
                        ):
                            session_ts[
                                self.get_problem()
                                .get_session(session)
                                .get_session_name()
                                + str(ts)
                            ].append(self.get_submissions_solution()[session][room][ts])

        for ts in session_ts.values():
            for this_sub in range(len(ts) - 1):
                for other_sub in range(this_sub + 1, len(ts)):
                    if (
                        self.get_problem()
                        .get_submission(ts[this_sub])
                        .get_submission_track()
                        .get_track_name()
                        == self.get_problem()
                        .get_submission(ts[other_sub])
                        .get_submission_track()
                        .get_track_name()
                    ) and (
                        (
                            self.get_problem()
                            .get_submission(ts[this_sub])
                            .get_submission_order()
                            != 0
                        )
                        and (
                            self.get_problem()
                            .get_submission(ts[other_sub])
                            .get_submission_order()
                            != 0
                        )
                    ):
                        p11_list.append(
                            self.get_problem()
                            .get_submission(ts[this_sub])
                            .get_submission_name()
                        )
                        p11_pen.append(
                            self.get_problem().get_parameters().submissions_order_weight
                        )

        for track in range(self.get_problem().get_number_of_tracks()):
            order = 1
            for sub in di[track]:
                if (
                    self.get_problem().get_submission(sub).get_submission_order()
                    != order
                ) and (
                    self.get_problem().get_submission(sub).get_submission_order() != 0
                ):
                    p11_list.append(
                        self.get_problem().get_submission(sub).get_submission_name()
                    )
                    p11_pen.append(
                        self.get_problem().get_parameters().submissions_order_weight
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
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(len(self.get_submissions_solution()[i][j])):
                    if self.get_submissions_solution()[i][j][x] != -1:
                        if (
                            self.get_problem().get_submissions_sessions_penalty_by_index(
                                self.get_submissions_solution()[i][j][x], i
                            )
                            != 0
                        ):
                            p12_list.append(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[i][j][x]
                                )
                                .get_submission_name()
                                + " - "
                                + self.get_problem().get_session(i).get_session_name()
                            )
                            p12_pen.append(
                                self.get_problem()
                                .get_parameters()
                                .submissions_sessions_penalty_weight
                                * self.get_problem().get_submissions_sessions_penalty_by_index(
                                    self.get_submissions_solution()[i][j][x], i
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
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(len(self.get_submissions_solution()[i][j])):
                    if self.get_submissions_solution()[i][j][x] != -1:
                        if (
                            self.get_problem().get_submissions_rooms_penalty_by_index(
                                self.get_submissions_solution()[i][j][x], j
                            )
                            != 0
                        ):
                            p13_list.append(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[i][j][x]
                                )
                                .get_submission_name()
                                + " - "
                                + self.get_problem().get_room(j).get_room_name()
                            )
                            p13_pen.append(
                                self.get_problem()
                                .get_parameters()
                                .submissions_rooms_penalty_weight
                                * self.get_problem().get_submissions_rooms_penalty_by_index(
                                    self.get_submissions_solution()[i][j][x], j
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
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(len(self.get_submissions_solution()[i][j])):
                    if (
                        (self.get_submissions_solution()[i][j][x] != -1)
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[i][j][x]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.get_submissions_solution()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.get_submissions_solution()[i][j][x], j))
        for i in range(len(self.get_tracks_solution())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.get_problem().get_submission(di[i][j][0])
                            in self.get_problem()
                            .get_submission(di[i][z][0])
                            .get_submission_presenter_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            p14_list.append(
                                str(
                                    self.get_problem()
                                    .get_submission(di[i][j][0])
                                    .get_submission_name()
                                )
                                + " - "
                                + str(
                                    self.get_problem()
                                    .get_submission(di[i][z][0])
                                    .get_submission_name()
                                )
                            )
                            p14_pen.append(
                                self.get_problem()
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
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                for x in range(len(self.get_submissions_solution()[i][j])):
                    if (
                        (self.get_submissions_solution()[i][j][x] != -1)
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[i][j][x]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and ((self.get_submissions_solution()[i][j][x], j) not in di[i])
                    ):
                        di[i].append((self.get_submissions_solution()[i][j][x], j))
        for i in range(len(self.get_tracks_solution())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.get_problem().get_submission(di[i][j][0])
                            in self.get_problem()
                            .get_submission(di[i][z][0])
                            .get_submission_attendee_conflicts_list()
                        ) and (di[i][j][1] != di[i][z][1]):
                            p15_list.append(
                                self.get_problem()
                                .get_submission(di[i][j][0])
                                .get_submission_name()
                                + " - "
                                + self.get_problem()
                                .get_submission(di[i][z][0])
                                .get_submission_name()
                            )
                            p15_pen.append(
                                self.get_problem()
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
            session: []
            for session in range(self.get_problem().get_number_of_sessions())
        }
        for i in range(len(self.get_tracks_solution())):
            for j in range(len(self.get_tracks_solution()[i])):
                if (self.get_tracks_solution()[i][j] != -1) and (
                    len(
                        self.get_problem()
                        .get_track(self.get_tracks_solution()[i][j])
                        .get_track_chair_conflicts_list()
                    )
                    != 0
                ):
                    di[i].append(self.get_tracks_solution()[i][j])
        for i in range(len(self.get_tracks_solution())):
            if len(di[i]) > 1:
                for j in range(len(di[i]) - 1):
                    for z in range(j + 1, len(di[i])):
                        if (
                            self.get_problem().get_track(di[i][j])
                            in self.get_problem()
                            .get_track(di[i][z])
                            .get_track_chair_conflicts_list()
                        ):
                            p16_list.append(
                                self.get_problem().get_track(di[i][j]).get_track_name()
                                + " - "
                                + self.get_problem()
                                .get_track(di[i][z])
                                .get_track_name()
                            )
                            p16_pen.append(
                                self.get_problem()
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
            for session in range(self.get_problem().get_number_of_sessions())
            for ts in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for ts in range(len(self.get_submissions_solution()[session][room])):
                    if (
                        (self.get_submissions_solution()[session][room][ts] != -1)
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][ts]
                                )
                                .get_submission_presenter_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.get_submissions_solution()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.get_submissions_solution()[session][room][ts]
                        )
        for session in range(len(self.get_tracks_solution())):
            for ts in range(len(self.get_submissions_solution()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.get_problem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.get_problem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_presenter_conflicts_list()
                            ):
                                p19_list.append(
                                    str(
                                        self.get_problem()
                                        .get_submission(di[str(session) + str(ts)][j])
                                        .get_submission_name()
                                    )
                                    + " - "
                                    + str(
                                        self.get_problem()
                                        .get_submission(di[str(session) + str(ts)][z])
                                        .get_submission_name()
                                    )
                                )
                                p19_pen.append(
                                    self.get_problem()
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
            for session in range(self.get_problem().get_number_of_sessions())
            for ts in range(
                self.get_problem().get_session(session).get_session_max_time_slots()
            )
        }
        for session in range(len(self.get_tracks_solution())):
            for room in range(len(self.get_tracks_solution()[session])):
                for ts in range(len(self.get_submissions_solution()[session][room])):
                    if (
                        (self.get_submissions_solution()[session][room][ts] != -1)
                        and (
                            len(
                                self.get_problem()
                                .get_submission(
                                    self.get_submissions_solution()[session][room][ts]
                                )
                                .get_submission_attendee_conflicts_list()
                            )
                            != 0
                        )
                        and (
                            self.get_submissions_solution()[session][room][ts]
                            not in di[str(session) + str(ts)]
                        )
                    ):
                        di[str(session) + str(ts)].append(
                            self.get_submissions_solution()[session][room][ts]
                        )
        for session in range(len(self.get_tracks_solution())):
            for ts in range(len(self.get_submissions_solution()[session][room])):
                if len(di[str(session) + str(ts)]) > 1:
                    for j in range(len(di[str(session) + str(ts)]) - 1):
                        for z in range(j + 1, len(di[str(session) + str(ts)])):
                            if (
                                self.get_problem().get_submission(
                                    di[str(session) + str(ts)][j]
                                )
                                in self.get_problem()
                                .get_submission(di[str(session) + str(ts)][z])
                                .get_submission_attendee_conflicts_list()
                            ):
                                p20_list.append(
                                    self.get_problem()
                                    .get_submission(di[str(session) + str(ts)][j])
                                    .get_submission_name()
                                    + " - "
                                    + self.get_problem()
                                    .get_submission(di[str(session) + str(ts)][z])
                                    .get_submission_name()
                                )
                                p20_pen.append(
                                    self.get_problem()
                                    .get_parameters()
                                    .attendees_conflicts_timeslot_level_weight
                                )
        p20_list.append("Total")
        p20_pen.append(sum(p20_pen))
        p20_pen.insert(0, "")
        df42 = pd.DataFrame(p20_list)
        df43 = pd.DataFrame(p20_pen)

        # Writing to excel file
        with pd.ExcelWriter(file_path) as writer:
            # Sol tracks
            df.to_excel(writer, sheet_name="sol")
            # Sol submissions
            df2.to_excel(
                writer,
                sheet_name="sol",
                startrow=self.get_problem().get_number_of_sessions() + 2,
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
        logging.info(f"Solution saved at {file_path}")

    def load_solution(self, file_path: Path) -> None:
        # Creating temporary tracks solution
        file = pd.read_excel(
            file_path, header=None, keep_default_na=False, na_filter=False
        )
        temp2 = []
        for session in range(1, self.get_problem().get_number_of_sessions() + 1):
            temp = []
            for room in range(1, len(file.keys())):
                if file.iloc[session][room] != "":
                    temp.append(
                        self.get_problem().get_track_index(file.iloc[session][room])
                    )
                else:
                    temp.append(-1)
            temp2.append(temp)

        # Converting temporary tracks solution into permanent tracks solution
        for session in range(len(temp2)):
            for room in range(len(temp2[session])):
                self.get_tracks_solution()[session][room] = temp2[session][room]

        # Creating temporary submissions solution
        temp3 = []
        sum_ts = 0
        for session in range(self.get_problem().get_number_of_sessions()):
            index = self.get_problem().get_number_of_sessions() + 1 + sum_ts
            temp2 = []
            for room in range(1, len(file.keys())):
                temp = []
                for ts in range(
                    self.get_problem().get_session(session).get_session_max_time_slots()
                ):
                    index += 1
                    if file.iloc[index][room] != "":
                        temp.append(
                            self.get_problem().get_submission_index(
                                file.iloc[index][room]
                            )
                        )
                    else:
                        temp.append(-1)
                index = self.get_problem().get_number_of_sessions() + 1 + sum_ts
                temp2.append(temp)
            temp3.append(temp2)
            sum_ts += (
                self.get_problem().get_session(session).get_session_max_time_slots()
            )

        # Converting temporary submissions solution into permanent submissions solution
        for session in range(len(temp3)):
            for room in range(len(temp3[session])):
                for ts in range(
                    self.get_problem().get_session(session).get_session_max_time_slots()
                ):
                    self.get_submissions_solution()[session][room][ts] = temp3[session][
                        room
                    ][ts]


class RandomIndirectSolution(Solution):
    def __init__(self, problem: Problem) -> None:
        self.__problem: Problem = problem
        Solution.__init__(self, problem)
        multi_slot_submissions = [
            submission
            for submission in range(self.__problem.get_number_of_submissions())
            if self.__problem.get_submission(
                submission
            ).get_submission_required_time_slots()
            > 1
        ]
        single_slot_submissions = [
            submission
            for submission in range(self.__problem.get_number_of_submissions())
            if self.__problem.get_submission(
                submission
            ).get_submission_required_time_slots()
            == 1
        ]
        sessions = [
            session for session in range(self.__problem.get_number_of_sessions())
        ]
        rooms = [room for room in range(self.__problem.get_number_of_rooms())]
        np.random.shuffle(sessions)
        np.random.shuffle(rooms)
        while True:
            np.random.shuffle(multi_slot_submissions)
            for submission in multi_slot_submissions:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if (
                            (
                                self.__problem.get_submission(
                                    submission
                                ).get_submission_required_time_slots()
                                <= self.get_submissions_solution()[session][room].count(
                                    -1
                                )
                            )
                            and (
                                self.__problem.get_track_index(
                                    self.__problem.get_submission(submission)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                                == self.get_tracks_solution()[session][room]
                            )
                        ) or (
                            (
                                self.__problem.get_submission(
                                    submission
                                ).get_submission_required_time_slots()
                                <= self.get_submissions_solution()[session][room].count(
                                    -1
                                )
                            )
                            and (self.get_tracks_solution()[session][room] == -1)
                        ):
                            for time_slot in range(
                                self.__problem.get_submission(
                                    submission
                                ).get_submission_required_time_slots()
                            ):
                                available_time_slot = self.get_submissions_solution()[
                                    session
                                ][room].index(-1)
                                self.get_submissions_solution()[session][room][
                                    available_time_slot
                                ] = submission
                            stop = True
                            self.get_tracks_solution()[session][room] = (
                                self.__problem.get_track_index(
                                    self.__problem.get_submission(submission)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                            )
            np.random.shuffle(sessions)
            np.random.shuffle(rooms)
            np.random.shuffle(single_slot_submissions)
            for submission in single_slot_submissions:
                stop = False
                for session in sessions:
                    if stop == True:
                        break
                    for room in rooms:
                        if stop == True:
                            break
                        if (
                            (
                                self.__problem.get_submission(
                                    submission
                                ).get_submission_required_time_slots()
                                <= self.get_submissions_solution()[session][room].count(
                                    -1
                                )
                            )
                            and (
                                self.__problem.get_track_index(
                                    self.__problem.get_submission(submission)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                                == self.get_tracks_solution()[session][room]
                            )
                        ) or (
                            (
                                self.__problem.get_submission(
                                    submission
                                ).get_submission_required_time_slots()
                                <= self.get_submissions_solution()[session][room].count(
                                    -1
                                )
                            )
                            and (self.get_tracks_solution()[session][room] == -1)
                        ):
                            available_time_slot = self.get_submissions_solution()[
                                session
                            ][room].index(-1)
                            self.get_submissions_solution()[session][room][
                                available_time_slot
                            ] = submission
                            stop = True
                            self.get_tracks_solution()[session][room] = (
                                self.__problem.get_track_index(
                                    self.__problem.get_submission(submission)
                                    .get_submission_track()
                                    .get_track_name()
                                )
                            )

            if self.evaluate_all_submissions_scheduled() == True:
                submissions_indirect_solution = [
                    [] for i in range(self.__problem.get_number_of_tracks())
                ]
                for session in range(len(self.get_tracks_solution())):
                    for room in range(len(self.get_tracks_solution()[session])):
                        if self.get_tracks_solution()[session][room] != -1:
                            for time_slot in range(
                                len(self.get_submissions_solution()[session][room])
                            ):
                                if (
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                    != -1
                                ) and (
                                    self.get_submissions_solution()[session][room][
                                        time_slot
                                    ]
                                    not in submissions_indirect_solution[
                                        self.get_tracks_solution()[session][room]
                                    ]
                                ):
                                    submissions_indirect_solution[
                                        self.get_tracks_solution()[session][room]
                                    ].append(
                                        self.get_submissions_solution()[session][room][
                                            time_slot
                                        ]
                                    )
                self.set_submissions_indirect_solution(submissions_indirect_solution)

                for session in range(self.__problem.get_number_of_sessions()):
                    for room in range(self.__problem.get_number_of_rooms()):
                        if self.get_submissions_solution()[session][room].count(
                            -1
                        ) == len(self.get_submissions_solution()[session][room]):
                            self.get_tracks_solution()[session][room] = -1
                self.reset_submissions_solution()
                self.convert_solution()

                if self.evaluate_all_submissions_scheduled() == True:
                    return
                else:
                    self.reset_tracks_solution()
                    self.reset_submissions_solution()
                    self.reset_submissions_indirect_solution()
            else:
                self.reset_tracks_solution()
                self.reset_submissions_solution()
                self.reset_submissions_indirect_solution()

# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@author: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from domain.submission import Submission
from domain.track import Track
from domain.room import Room
from domain.session import Session
from parameters import Parameters
from typing import List, Dict
from pathlib import Path
import logging
import config
import pandas as pd
import datetime as dt
import pytz


class Problem:
    def __init__(self, file_path: Path) -> None:
        self.__file_name: str = file_path.stem
        self.__file_path: Path = file_path
        self.__file: dict[str, pd.DataFrame] = pd.read_excel(file_path, None)
        self.__check_all_sheets_exist()
        self.__submissions_file: pd.DataFrame = pd.read_excel(
            file_path,
            sheet_name="submissions",
            keep_default_na=False,
            na_filter=False,
        )
        self.__tracks_file: pd.DataFrame = pd.read_excel(
            file_path,
            sheet_name="tracks",
            keep_default_na=False,
            na_filter=False,
        )
        self.__processed_submissions_file: pd.DataFrame = None
        self.__parameters: Parameters = None

        self.__rooms: List[Room] = list()
        self.__sessions: List[Session] = list()
        self.__tracks: List[Track] = list()
        self.__submissions: List[Submission] = list()

        self.__rooms_map: Dict[str, int] = dict()
        self.__sessions_map: Dict[str, int] = dict()
        self.__tracks_map: Dict[str, int] = dict()
        self.__submissions_map: Dict[str, int] = dict()

        self.__submissions_sessions_penalty_map: Dict[str, int] = dict()
        self.__submissions_timezones_penalty_map: Dict[str, int] = dict()
        self.__submissions_rooms_penalty_map: Dict[str, int] = dict()
        self.__tracks_sessions_penalty_map: Dict[str, int] = dict()
        self.__tracks_rooms_penalty_map: Dict[str, int] = dict()
        self.__tracks_tracks_penalty_map: Dict[str, int] = dict()
        self.__sessions_rooms_penalty_map: Dict[str, int] = dict()

    def get_file_name(self) -> str:
        return self.__file_name

    def get_file_path(self) -> Path:
        return self.__file_path

    def build(self) -> None:
        logging.info(f"Building instance {self.__file_name}")
        self.__check_for_duplicates()

        self.__build_sessions()
        self.__build_rooms()
        self.__build_submissions()

        self.__set_track_session_penalties()
        self.__set_track_room_penalties()
        self.__set_track_track_penalties()
        self.__set_session_room_penalties()
        self.__set_parameters()

        self.__check_feasibility_of_problem()
        self.__set_conflicts()
        self.__set_timezone_penalties()

    def get_number_of_rooms(self) -> int:
        return len(self.__rooms)

    def get_room(self, index: int) -> Room:
        return self.__rooms[index]

    def get_room_list(self) -> List[Room]:
        return self.__rooms

    def get_room_index(self, room_name: str) -> int:
        return self.__rooms_map[room_name]

    def get_number_of_sessions(self) -> int:
        return len(self.__sessions)

    def get_session(self, index: int) -> Session:
        return self.__sessions[index]

    def get_session_list(self) -> List[Session]:
        return self.__sessions

    def get_session_index(self, session_name: str) -> int:
        return self.__sessions_map[session_name]

    def get_sum_of_available_time_slots(self) -> int:
        sum_of_time_slots = 0
        for session in self.__sessions:
            sum_of_time_slots += session.get_session_max_time_slots()
        return sum_of_time_slots

    def get_time_slots_from_largest_session(self) -> int:
        time_slots_list = []
        for session in self.__sessions:
            time_slots_list.append(session.get_session_max_time_slots())
        return max(time_slots_list)

    def get_number_of_tracks(self) -> int:
        return len(self.__tracks)

    def get_track(self, index: int) -> Track:
        return self.__tracks[index]

    def get_trackList(self) -> List[Track]:
        return self.__tracks

    def get_track_index(self, track_name: str) -> int:
        return self.__tracks_map[track_name]

    def get_number_of_submissions(self) -> int:
        return len(self.__submissions)

    def get_submission(self, index) -> Submission:
        return self.__submissions[index]

    def get_submissionList(self) -> List[Submission]:
        return self.__submissions

    def get_submission_index(self, submission_name: str) -> int:
        return self.__submissions_map[submission_name]

    def get_sum_of_required_time_slots(self) -> int:
        sum_of_required_time_slots = 0
        for submission in self.__submissions:
            sum_of_required_time_slots += (
                submission.get_submission_required_time_slots()
            )
        return sum_of_required_time_slots

    def get_parameters(self) -> Parameters:
        return self.__parameters

    def get_submissions_sessions_penalty(
        self, submission_name: str, session_name: str
    ) -> int:
        return self.__submissions_sessions_penalty_map[submission_name + session_name]

    def get_submissions_sessions_penalty_by_index(
        self, submission_index: int, session_index: int
    ) -> int:
        return self.__submissions_sessions_penalty_map[
            self.get_submission(submission_index).get_submission_name()
            + self.get_session(session_index).get_session_name()
        ]

    def get_submissions_timezones_penalty(
        self, submission_name: str, session_name: str
    ) -> int:
        return self.__submissions_timezones_penalty_map[submission_name + session_name]

    def get_submissions_timezones_penalty_by_index(
        self, submission_index: int, session_index: int
    ) -> int:
        return self.__submissions_timezones_penalty_map[
            self.get_submission(submission_index).get_submission_name()
            + self.get_session(session_index).get_session_name()
        ]

    def get_submissions_rooms_penalty(
        self, submission_name: str, room_name: str
    ) -> int:
        return self.__submissions_rooms_penalty_map[submission_name + room_name]

    def get_submissions_rooms_penalty_by_index(
        self, submission_index: int, room_index: int
    ) -> int:
        return self.__submissions_rooms_penalty_map[
            self.get_submission(submission_index).get_submission_name()
            + self.get_room(room_index).get_room_name()
        ]

    def get_tracks_sessions_penalty(self, track_name: str, session_name: str) -> int:
        return self.__tracks_sessions_penalty_map[track_name + session_name]

    def get_tracks_sessions_penalty_by_index(
        self, track_index: int, session_index: int
    ) -> int:
        return self.__tracks_sessions_penalty_map[
            self.get_track(track_index).get_track_name()
            + self.get_session(session_index).get_session_name()
        ]

    def get_tracks_rooms_penalty(self, track_name: str, room_name: str) -> int:
        return self.__tracks_rooms_penalty_map[track_name + room_name]

    def get_tracks_rooms_penalty_by_index(
        self, track_index: int, room_index: int
    ) -> int:
        return self.__tracks_rooms_penalty_map[
            self.get_track(track_index).get_track_name()
            + self.get_room(room_index).get_room_name()
        ]

    def get_tracks_tracks_penalty(
        self, this_track_name: str, other_track_name: str
    ) -> int:
        return self.__tracks_tracks_penalty_map[this_track_name + other_track_name]

    def get_tracks_tracks_penalty_by_index(
        self, this_track_index: int, other_track_index: int
    ) -> int:
        return self.__tracks_tracks_penalty_map[
            self.get_track(this_track_index).get_track_name()
            + self.get_track(other_track_index).get_track_name()
        ]

    def get_sessions_rooms_penalty(self, session_name: str, room_name: str) -> int:
        return self.__sessions_rooms_penalty_map[session_name + room_name]

    def get_sessions_rooms_penalty_by_index(
        self, session_index: int, room_index: int
    ) -> int:
        return self.__sessions_rooms_penalty_map[
            self.get_session(session_index).get_session_name()
            + self.get_room(room_index).get_room_name()
        ]

    def __build_sessions(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="sessions",
            keep_default_na=False,
            na_filter=False,
        )
        for row_index in range(len(file)):
            raw_start_time = str(file.iloc[row_index, 3]).split(":")
            raw_end_time = str(file.iloc[row_index, 4]).split(":")
            start_time = dt.datetime(
                2021, 7, 21, int(raw_start_time[0]), int(raw_start_time[1])
            )
            end_time = dt.datetime(
                2021, 7, 21, int(raw_end_time[0]), int(raw_end_time[1])
            )
            self.__set_session(
                Session(
                    file.iloc[row_index, 0],
                    file.iloc[row_index, 1],
                    file.iloc[row_index, 2],
                    start_time,
                    end_time,
                )
            )

    def __build_rooms(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="rooms",
            keep_default_na=False,
            na_filter=False,
        )
        for row_index in range(len(file)):
            self.__set_room(Room(file.iloc[row_index, 0]))

    def __build_tracks(self) -> None:
        for row_index in range(len(self.__tracks_file)):
            self.__set_track(
                Track(
                    self.__tracks_file.iloc[row_index, 0],
                    list(self.__tracks_file.iloc[row_index, 1].split(", ")),
                    list(),
                    list(),
                )
            )

    def __build_submissions(self) -> None:
        first_chunk = self.__submissions_file.iloc[:, : config.COLUMNS_TO_INCLUDE]
        first_chunk = first_chunk.replace({"Time Zone": config.TIMEZONE_MAPPING})
        second_chunk = self.__submissions_file.iloc[:, config.COLUMNS_TO_INCLUDE :]
        second_chunk.replace(to_replace="", value=0, inplace=True)

        self.__processed_submissions_file = first_chunk.join(second_chunk)
        tracks_frequency = self.__processed_submissions_file["Track"].value_counts(
            sort=False
        )

        self.__check_number_of_items_in_submissions_sheet()
        self.__check_for_invalid_tracks(tracks_frequency)
        self.__check_number_of_items_in_penalty_sheets()
        self.__check_naming_is_valid()

        self.__build_tracks()

        for row_index in range(len(self.__processed_submissions_file)):
            if self.__is_track_unknown(row_index):
                raise ValueError(
                    f"Track Error! \nUnknown track for {self.__processed_submissions_file.iloc[row_index, 0]} [ Track name: {self.__processed_submissions_file.iloc[row_index, 1]} ]."
                )

            self.__set_submission(
                Submission(
                    self.__processed_submissions_file.iloc[row_index, 0],
                    self.get_track(
                        self.get_track_index(
                            self.__processed_submissions_file.iloc[row_index, 1]
                        )
                    ),
                    self.__processed_submissions_file.iloc[row_index, 2],
                    self.__processed_submissions_file.iloc[row_index, 3],
                    self.__processed_submissions_file.iloc[row_index, 4],
                    list(
                        self.__processed_submissions_file.iloc[row_index, 5].split(", ")
                    ),
                    list(
                        self.__processed_submissions_file.iloc[row_index, 6].split(", ")
                    ),
                    list(),
                    list(),
                )
            )
            self.get_track(
                self.get_track_index(
                    self.__processed_submissions_file.iloc[row_index, 1]
                )
            ).set_track_submissions(
                self.get_submission(
                    self.get_submission_index(
                        self.__processed_submissions_file.iloc[row_index, 0]
                    )
                )
            )

            for column_index in range(
                config.COLUMNS_TO_INCLUDE,
                config.COLUMNS_TO_INCLUDE + self.get_number_of_sessions(),
            ):
                self.__set_submissions_sessions_penalty(
                    self.get_submission(
                        self.get_submission_index(
                            self.__processed_submissions_file.iloc[row_index, 0]
                        )
                    ).get_submission_name(),
                    self.get_session(
                        self.get_session_index(
                            self.__processed_submissions_file.columns[column_index]
                        )
                    ).get_session_name(),
                    self.__processed_submissions_file.iloc[row_index, column_index],
                )

            for column_index in range(
                config.COLUMNS_TO_INCLUDE + self.get_number_of_sessions(),
                config.COLUMNS_TO_INCLUDE
                + self.get_number_of_sessions()
                + self.get_number_of_rooms(),
            ):
                self.__set_submissions_rooms_penalty(
                    self.get_submission(
                        self.get_submission_index(
                            self.__processed_submissions_file.iloc[row_index, 0]
                        )
                    ).get_submission_name(),
                    self.get_room(
                        self.get_room_index(
                            self.__processed_submissions_file.columns[column_index]
                        )
                    ).get_room_name(),
                    self.__processed_submissions_file.iloc[row_index, column_index],
                )

        for track_index in range(self.get_number_of_tracks()):
            required_time_slots = []
            for submission in self.get_track(track_index).get_track_submissions_list():
                required_time_slots.append(
                    submission.get_submission_required_time_slots()
                )
            self.get_track(track_index).set_track_required_time_slots(
                sum(required_time_slots)
            )

    def __set_track_session_penalties(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="tracks_sessions|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__set_tracks_sessions_penalty(
                    self.get_track(
                        self.get_track_index(file.iloc[row_index, 0])
                    ).get_track_name(),
                    self.get_session(
                        self.get_session_index(columns[column_index])
                    ).get_session_name(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_track_room_penalties(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="tracks_rooms|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__set_tracks_rooms_penalty(
                    self.get_track(
                        self.get_track_index(file.iloc[row_index, 0])
                    ).get_track_name(),
                    self.get_room(
                        self.get_room_index(columns[column_index])
                    ).get_room_name(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_track_track_penalties(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="similar tracks",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        penalty_list = file.values.tolist()

        for i in range(len(penalty_list)):
            for y in range(len(penalty_list)):
                if y != i:
                    self.__set_tracks_tracks_penalty(
                        self.get_track(
                            self.get_track_index(penalty_list[i][0])
                        ).get_track_name(),
                        self.get_track(
                            self.get_track_index(penalty_list[y][0])
                        ).get_track_name(),
                        penalty_list[y][i + 1],
                    )
                    self.__set_tracks_tracks_penalty(
                        self.get_track(
                            self.get_track_index(penalty_list[y][0])
                        ).get_track_name(),
                        self.get_track(
                            self.get_track_index(penalty_list[i][0])
                        ).get_track_name(),
                        penalty_list[y][i + 1],
                    )

    def __set_session_room_penalties(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="sessions_rooms|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__set_sessions_rooms_penalty(
                    self.get_session(
                        self.get_session_index(file.iloc[row_index, 0])
                    ).get_session_name(),
                    self.get_room(
                        self.get_room_index(columns[column_index])
                    ).get_room_name(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_parameters(self) -> None:
        file = pd.read_excel(
            self.get_file_path(),
            sheet_name="parameters",
            keep_default_na=False,
            na_filter=False,
        )
        file = file.replace({"Unnamed: 1": config.TIMEZONE_MAPPING})
        file = file.map(lambda x: str(x).split(":"))

        self.__parameters = Parameters(
            local_time_zone=file.iloc[0, 1][0],
            suitable_schedule_time_from=file.iloc[2, 1],
            suitable_schedule_time_to=file.iloc[3, 1],
            less_suitable_schedule_time_from=file.iloc[5, 1],
            less_suitable_schedule_time_to=file.iloc[6, 1],
            tracks_sessions_penalty_weight=int(file.iloc[0, 4][0]),
            tracks_rooms_penalty_weight=int(file.iloc[1, 4][0]),
            sessions_rooms_penalty_weight=int(file.iloc[2, 4][0]),
            similar_tracks_penalty_weight=int(file.iloc[3, 4][0]),
            num_rooms_per_track_weight=int(file.iloc[4, 4][0]),
            parallel_tracks_weight=int(file.iloc[5, 4][0]),
            consecutive_tracks_weight=int(file.iloc[6, 4][0]),
            submissions_timezones_penalty_weight=int(file.iloc[7, 4][0]),
            submissions_order_weight=int(file.iloc[8, 4][0]),
            submissions_sessions_penalty_weight=int(file.iloc[9, 4][0]),
            submissions_rooms_penalty_weight=int(file.iloc[10, 4][0]),
            presenters_conflicts_weight=int(file.iloc[11, 4][0]),
            attendees_conflicts_weight=int(file.iloc[12, 4][0]),
            chairs_conflicts_weight=int(file.iloc[13, 4][0]),
            presenters_conflicts_timeslot_level_weight=int(file.iloc[14, 4][0]),
            attendees_conflicts_timeslot_level_weight=int(file.iloc[15, 4][0]),
            small_timezone_penalty=int(file.iloc[7, 1][0]),
            big_timezone_penalty=int(file.iloc[9, 1][0]),
        )

    def __set_track(self, track: Track):
        self.__tracks.append(track)
        self.__tracks_map[track.get_track_name()] = len(self.__tracks_map)

    def __set_submission(self, submission: Submission):
        self.__submissions.append(submission)
        self.__submissions_map[submission.get_submission_name()] = len(
            self.__submissions_map
        )

    def __set_submissions_sessions_penalty(
        self, submission_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__submissions_sessions_penalty_map[submission_name + session_name] = (
            penalty_value
        )

    def __set_submissions_timezones_penalty(
        self, submission_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__submissions_timezones_penalty_map[submission_name + session_name] = (
            penalty_value
        )

    def __set_submissions_rooms_penalty(
        self, submission_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__submissions_rooms_penalty_map[submission_name + room_name] = (
            penalty_value
        )

    def __set_tracks_sessions_penalty(
        self, track_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__tracks_sessions_penalty_map[track_name + session_name] = penalty_value

    def __set_tracks_rooms_penalty(
        self, track_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__tracks_rooms_penalty_map[track_name + room_name] = penalty_value

    def __set_tracks_tracks_penalty(
        self, this_track_name: str, other_track_name: str, penalty_value: int
    ) -> None:
        self.__tracks_tracks_penalty_map[this_track_name + other_track_name] = (
            penalty_value
        )

    def __set_sessions_rooms_penalty(
        self, session_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__sessions_rooms_penalty_map[session_name + room_name] = penalty_value

    def __check_feasibility_of_problem(self) -> None:
        if (
            self.get_sum_of_available_time_slots() * self.get_number_of_rooms()
            < self.get_sum_of_required_time_slots()
        ):
            raise ValueError(
                "Infeasible!: Not Enough Time Slots Available!\nConsider to add an extra session or room."
            )

    def __set_conflicts(self) -> None:
        for i in range(self.get_number_of_submissions()):
            for y in range(self.get_number_of_submissions()):
                if y != i:
                    for x in range(
                        len(self.get_submission(i).get_submission_attendees_list())
                    ):
                        if (
                            self.get_submission(i).get_submission_attendees_list()[x]
                            != ""
                        ):
                            for z in range(
                                len(
                                    self.get_submission(
                                        y
                                    ).get_submission_attendees_list()
                                )
                            ):
                                if (
                                    self.get_submission(
                                        i
                                    ).get_submission_attendees_list()[x]
                                    == self.get_submission(
                                        y
                                    ).get_submission_attendees_list()[z]
                                ):
                                    self.get_submission(
                                        i
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(y)
                                    )
                                    self.get_submission(
                                        y
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(i)
                                    )
                    for x in range(
                        len(self.get_submission(i).get_submission_attendees_list())
                    ):
                        if (
                            self.get_submission(i).get_submission_attendees_list()[x]
                            != ""
                        ):
                            for z in range(
                                len(
                                    self.get_submission(
                                        y
                                    ).get_submission_prsenters_list()
                                )
                            ):
                                if (
                                    self.get_submission(
                                        i
                                    ).get_submission_attendees_list()[x]
                                    == self.get_submission(
                                        y
                                    ).get_submission_prsenters_list()[z]
                                ):
                                    self.get_submission(
                                        i
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(y)
                                    )
                                    self.get_submission(
                                        y
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(i)
                                    )
                    for x in range(
                        len(self.get_submission(i).get_submission_attendees_list())
                    ):
                        if (
                            self.get_submission(i).get_submission_attendees_list()[x]
                            != ""
                        ):
                            for z in range(
                                len(
                                    self.get_submission(y)
                                    .get_submission_track()
                                    .get_track_chairs_list()
                                )
                            ):
                                if (
                                    self.get_submission(
                                        i
                                    ).get_submission_attendees_list()[x]
                                    == self.get_submission(y)
                                    .get_submission_track()
                                    .get_track_chairs_list()[z]
                                ) and (
                                    self.get_submission(i).get_submission_track()
                                    != self.get_submission(y).get_submission_track()
                                ):
                                    self.get_submission(
                                        i
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(y)
                                    )
                                    self.get_submission(
                                        y
                                    ).set_submission_attendee_conflicts(
                                        self.get_submission(i)
                                    )

    def __set_timezone_penalties(self) -> None:
        parameters = self.get_parameters()
        suitable_from = dt.datetime(
            2021,
            7,
            21,
            int(parameters.suitable_schedule_time_from[0]),
            int(parameters.suitable_schedule_time_from[1]),
        ).time()
        suitable_to = dt.datetime(
            2021,
            7,
            21,
            int(parameters.suitable_schedule_time_to[0]),
            int(parameters.suitable_schedule_time_to[1]),
        ).time()
        less_suitable_from = dt.datetime(
            2021,
            7,
            21,
            int(parameters.less_suitable_schedule_time_from[0]),
            int(parameters.less_suitable_schedule_time_from[1]),
        ).time()
        less_suitable_to = dt.datetime(
            2021,
            7,
            21,
            int(parameters.less_suitable_schedule_time_to[0]),
            int(parameters.less_suitable_schedule_time_to[1]),
        ).time()
        for session_index in range(self.get_number_of_sessions()):
            # Defining session's local time zone
            loc_tz_st = (
                self.get_session(session_index)
                .get_session_start_time()
                .replace(tzinfo=pytz.timezone(parameters.local_time_zone))
            )
            loc_tz_et = (
                self.get_session(session_index)
                .get_session_end_time()
                .replace(tzinfo=pytz.timezone(parameters.local_time_zone))
            )
            for submission_index in range(self.get_number_of_submissions()):
                # Defining submission's time zone
                submission_tz = pytz.timezone(
                    self.get_submission(submission_index).get_submission_timezone()
                )
                # Removing dates
                start_time = loc_tz_st.astimezone(submission_tz).time()
                end_time = loc_tz_et.astimezone(submission_tz).time()
                # Assigning submissionstimezones|penalty
                if (
                    start_time < less_suitable_from
                    or end_time > less_suitable_to
                    or end_time < less_suitable_from
                ):
                    self.__set_submissions_timezones_penalty(
                        self.get_submission(submission_index).get_submission_name(),
                        self.get_session(session_index).get_session_name(),
                        parameters.big_timezone_penalty,
                    )
                elif (
                    start_time >= less_suitable_from and start_time < suitable_from
                ) or (end_time > suitable_to and end_time <= less_suitable_to):
                    self.__set_submissions_timezones_penalty(
                        self.get_submission(submission_index).get_submission_name(),
                        self.get_session(session_index).get_session_name(),
                        parameters.small_timezone_penalty,
                    )
                else:
                    self.__set_submissions_timezones_penalty(
                        self.get_submission(submission_index).get_submission_name(),
                        self.get_session(session_index).get_session_name(),
                        0,
                    )

    def __set_session(self, session: Session) -> None:
        self.__sessions.append(session)
        self.__sessions_map[session.get_session_name()] = len(self.__sessions_map)

    def __set_room(self, room: Room) -> None:
        self.__rooms.append(room)
        self.__rooms_map[room.get_room_name()] = len(self.__rooms_map)

    def __check_all_sheets_exist(self) -> None:
        existing_sheets = self.__file.keys()
        for sheet in config.REQUIRED_SHEETS:
            if sheet not in existing_sheets:
                raise ValueError(f"Missing Sheet Error! \nMissing Sheet: {sheet}")

    def __check_for_duplicates(self) -> None:
        cols = list(
            pd.read_excel(
                self.get_file_path(), sheet_name="submissions", header=None, nrows=1
            ).values[0]
        )
        if len(cols) != len(set(cols)):
            raise ValueError(
                "Duplicates Error! \nDuplicate column names found in submissions sheet!"
            )

        duplicates_check = ["submissions", "tracks", "sessions", "rooms"]
        for sheet in duplicates_check:
            duplicates = self.__file[sheet].duplicated(
                subset=self.__file[sheet].columns[0]
            )
            if duplicates.any() == True:
                duplicate_indexes = duplicates[duplicates].index
                raise ValueError(
                    f"Duplicates Error! \nThe following duplicates were found in sheet {sheet}: \n{self.__file[sheet][self.__file[sheet].columns[0]][duplicate_indexes]}"
                )

        duplicates_check = [
            "tracks_sessions|penalty",
            "tracks_rooms|penalty",
            "similar tracks",
            "sessions_rooms|penalty",
        ]
        for sheet in duplicates_check:
            cols = list(
                pd.read_excel(
                    self.get_file_path(), sheet_name=sheet, header=None, nrows=1
                ).values[0]
            )
            if len(cols) != len(set(cols)):
                raise ValueError(
                    "Duplicates Error! \nDuplicate column names found in submissions sheet!"
                )
            duplicate_row = self.__file[sheet].iloc[:, 0].duplicated()
            if duplicate_row.any() == True:
                duplicate_indexes = duplicate_row[duplicate_row].index
                raise ValueError(
                    f"Duplicates Error! \nThe following duplicates were found in sheet {sheet}: \n{self.__file[sheet][self.__file[sheet].columns[0]][duplicate_indexes]}"
                )

    def __check_for_invalid_tracks(self, tracks_frequency: pd.Series) -> None:
        for track in self.__tracks_file["Tracks"].values:
            if track not in tracks_frequency.keys():
                raise ValueError(
                    f"Track Error!\nTrack Name: {track} has none submissions!"
                )

    def __check_number_of_items_in_penalty_sheets(self) -> None:
        file = pd.read_excel(self.get_file_path(), None, header=None)
        if (
            len(file["tracks_sessions|penalty"].iloc[0, :]) != len(file["sessions"])
        ) or (len(file["tracks_sessions|penalty"].iloc[:, 0]) != len(file["tracks"])):
            raise ValueError(
                "Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_sessions|penalty."
            )
        if (len(file["tracks_rooms|penalty"].iloc[0, :]) != len(file["rooms"])) or (
            len(file["tracks_rooms|penalty"].iloc[:, 0]) != len(file["tracks"])
        ):
            raise ValueError(
                "Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_rooms|penalty."
            )
        if (len(file["similar tracks"].iloc[0, :]) != len(file["tracks"])) or (
            len(file["similar tracks"].iloc[:, 0]) != len(file["tracks"])
        ):
            raise ValueError(
                "Incorrect Number of Items Error! \nIncorrect number of items in sheet tracks_tracks|penalty."
            )
        if (len(file["sessions_rooms|penalty"].iloc[0, :]) != len(file["rooms"])) or (
            len(file["sessions_rooms|penalty"].iloc[:, 0]) != len(file["sessions"])
        ):
            raise ValueError(
                "Incorrect Number of Items Error! \nIncorrect number of items in sheet sessions_rooms|penalty."
            )

    def __check_number_of_items_in_submissions_sheet(self) -> None:
        if (
            len(self.__processed_submissions_file.columns[config.COLUMNS_TO_INCLUDE :])
            != self.get_number_of_sessions() + self.get_number_of_rooms()
        ):
            raise ValueError(
                "Incorrect Number of Items Error! \nEnsure that number of sessions and rooms in sheet submissions match with number of itmes in sessions and rooms sheets."
            )

    def __check_naming_is_valid(self) -> None:
        for session_index in range(self.get_number_of_sessions()):
            if (
                self.get_session(session_index).get_session_name()
                not in self.__processed_submissions_file.columns[
                    config.COLUMNS_TO_INCLUDE : config.COLUMNS_TO_INCLUDE
                    + self.get_number_of_sessions()
                ]
            ):
                raise ValueError(
                    "Sessions Error!\nSessions names in submissions sheet must match those in sessions sheet."
                )

        for room_index in range(self.get_number_of_rooms()):
            if (
                self.get_room(room_index).get_room_name()
                not in self.__processed_submissions_file.columns[
                    config.COLUMNS_TO_INCLUDE
                    + self.get_number_of_sessions() : config.COLUMNS_TO_INCLUDE
                    + self.get_number_of_sessions()
                    + self.get_number_of_rooms()
                ]
            ):
                raise ValueError(
                    "Rooms Error!\nRooms names in submissions sheet must match those in rooms sheet."
                )

    def __is_track_unknown(self, row_index: int) -> bool:
        return (
            self.__processed_submissions_file.iloc[row_index, 1]
            not in self.__tracks_file["Tracks"].values
        )

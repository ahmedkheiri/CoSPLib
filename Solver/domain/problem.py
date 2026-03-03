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

    def getFileName(self) -> str:
        return self.__file_name

    def getFilePath(self) -> Path:
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

    def getNumberOfRooms(self) -> int:
        return len(self.__rooms)

    def getRoom(self, index: int) -> Room:
        return self.__rooms[index]

    def getRoomList(self) -> List[Room]:
        return self.__rooms

    def getRoomIndex(self, room_name: str) -> int:
        return self.__rooms_map[room_name]

    def getNumberOfSessions(self) -> int:
        return len(self.__sessions)

    def getSession(self, index: int) -> Session:
        return self.__sessions[index]

    def getSessionList(self) -> List[Session]:
        return self.__sessions

    def getSessionIndex(self, session_name: str) -> int:
        return self.__sessions_map[session_name]

    def getSumOfAvailableTimeSlots(self) -> int:
        sum_of_time_slots = 0
        for session in self.__sessions:
            sum_of_time_slots += session.getSessionMaxTimeSlots()
        return sum_of_time_slots

    def getLargestSessionTimeSlots(self) -> int:
        time_slots_list = []
        for session in self.__sessions:
            time_slots_list.append(session.getSessionMaxTimeSlots())
        return max(time_slots_list)

    def getNumberOfTracks(self) -> int:
        return len(self.__tracks)

    def getTrack(self, index: int) -> Track:
        return self.__tracks[index]

    def getTrackList(self) -> List[Track]:
        return self.__tracks

    def getTrackIndex(self, track_name: str) -> int:
        return self.__tracks_map[track_name]

    def getNumberOfSubmissions(self) -> int:
        return len(self.__submissions)

    def getSubmission(self, index) -> Submission:
        return self.__submissions[index]

    def getSubmissionList(self) -> List[Submission]:
        return self.__submissions

    def getSubmissionIndex(self, submission_name: str) -> int:
        return self.__submissions_map[submission_name]

    def getSumOfRequiredTimeSlots(self) -> int:
        sum_of_required_time_slots = 0
        for submission in self.__submissions:
            sum_of_required_time_slots += submission.getSubmissionRequiredTimeSlots()
        return sum_of_required_time_slots

    def getParameters(self) -> Parameters:
        return self.__parameters

    def getSubmissionsSessionsPenalty(
        self, submission_name: str, session_name: str
    ) -> int:
        return self.__submissions_sessions_penalty_map[submission_name + session_name]

    def getSubmissionsSessionsPenaltybyIndex(
        self, submission_index: int, session_index: int
    ) -> int:
        return self.__submissions_sessions_penalty_map[
            self.getSubmission(submission_index).getSubmissionName()
            + self.getSession(session_index).getSessionName()
        ]

    def getSubmissionsTimezonesPenalty(
        self, submission_name: str, session_name: str
    ) -> int:
        return self.__submissions_timezones_penalty_map[submission_name + session_name]

    def getSubmissionsTimezonesPenaltybyIndex(
        self, submission_index: int, session_index: int
    ) -> int:
        return self.__submissions_timezones_penalty_map[
            self.getSubmission(submission_index).getSubmissionName()
            + self.getSession(session_index).getSessionName()
        ]

    def getSubmissionsRoomsPenalty(self, submission_name: str, room_name: str) -> int:
        return self.__submissions_rooms_penalty_map[submission_name + room_name]

    def getSubmissionsRoomsPenaltybyIndex(
        self, submission_index: int, room_index: int
    ) -> int:
        return self.__submissions_rooms_penalty_map[
            self.getSubmission(submission_index).getSubmissionName()
            + self.getRoom(room_index).getRoomName()
        ]

    def getTracksSessionsPenalty(self, track_name: str, session_name: str) -> int:
        return self.__tracks_sessions_penalty_map[track_name + session_name]

    def getTracksSessionsPenaltybyIndex(
        self, track_index: int, session_index: int
    ) -> int:
        return self.__tracks_sessions_penalty_map[
            self.getTrack(track_index).getTrackName()
            + self.getSession(session_index).getSessionName()
        ]

    def getTracksRoomsPenalty(self, track_name: str, room_name: str) -> int:
        return self.__tracks_rooms_penalty_map[track_name + room_name]

    def getTracksRoomsPenaltybyIndex(self, track_index: int, room_index: int) -> int:
        return self.__tracks_rooms_penalty_map[
            self.getTrack(track_index).getTrackName()
            + self.getRoom(room_index).getRoomName()
        ]

    def getTracksTracksPenalty(
        self, this_track_name: str, other_track_name: str
    ) -> int:
        return self.__tracks_tracks_penalty_map[this_track_name + other_track_name]

    def getTracksTracksPenaltybyIndex(
        self, this_track_index: int, other_track_index: int
    ) -> int:
        return self.__tracks_tracks_penalty_map[
            self.getTrack(this_track_index).getTrackName()
            + self.getTrack(other_track_index).getTrackName()
        ]

    def getSessionsRoomsPenalty(self, session_name: str, room_name: str) -> int:
        return self.__sessions_rooms_penalty_map[session_name + room_name]

    def getSessionsRoomsPenaltybyIndex(
        self, session_index: int, room_index: int
    ) -> int:
        return self.__sessions_rooms_penalty_map[
            self.getSession(session_index).getSessionName()
            + self.getRoom(room_index).getRoomName()
        ]

    def __build_sessions(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
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
            self.__setSession(
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
            self.getFilePath(),
            sheet_name="rooms",
            keep_default_na=False,
            na_filter=False,
        )
        for row_index in range(len(file)):
            self.__setRoom(Room(file.iloc[row_index, 0]))

    def __build_tracks(self) -> None:
        for row_index in range(len(self.__tracks_file)):
            self.__setTrack(
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

            self.__setSubmission(
                Submission(
                    self.__processed_submissions_file.iloc[row_index, 0],
                    self.getTrack(
                        self.getTrackIndex(
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
            self.getTrack(
                self.getTrackIndex(self.__processed_submissions_file.iloc[row_index, 1])
            ).setTrackSubmissions(
                self.getSubmission(
                    self.getSubmissionIndex(
                        self.__processed_submissions_file.iloc[row_index, 0]
                    )
                )
            )

            for column_index in range(
                config.COLUMNS_TO_INCLUDE,
                config.COLUMNS_TO_INCLUDE + self.getNumberOfSessions(),
            ):
                self.__setSubmissionsSessionsPenalty(
                    self.getSubmission(
                        self.getSubmissionIndex(
                            self.__processed_submissions_file.iloc[row_index, 0]
                        )
                    ).getSubmissionName(),
                    self.getSession(
                        self.getSessionIndex(
                            self.__processed_submissions_file.columns[column_index]
                        )
                    ).getSessionName(),
                    self.__processed_submissions_file.iloc[row_index, column_index],
                )

            for column_index in range(
                config.COLUMNS_TO_INCLUDE + self.getNumberOfSessions(),
                config.COLUMNS_TO_INCLUDE
                + self.getNumberOfSessions()
                + self.getNumberOfRooms(),
            ):
                self.__setSubmissionsRoomsPenalty(
                    self.getSubmission(
                        self.getSubmissionIndex(
                            self.__processed_submissions_file.iloc[row_index, 0]
                        )
                    ).getSubmissionName(),
                    self.getRoom(
                        self.getRoomIndex(
                            self.__processed_submissions_file.columns[column_index]
                        )
                    ).getRoomName(),
                    self.__processed_submissions_file.iloc[row_index, column_index],
                )

        for track_index in range(self.getNumberOfTracks()):
            required_time_slots = []
            for submission in self.getTrack(track_index).getTrackSubmissionsList():
                required_time_slots.append(submission.getSubmissionRequiredTimeSlots())
            self.getTrack(track_index).setTrackRequiredTimeSlots(
                sum(required_time_slots)
            )

    def __set_track_session_penalties(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
            sheet_name="tracks_sessions|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__setTracksSessionsPenalty(
                    self.getTrack(
                        self.getTrackIndex(file.iloc[row_index, 0])
                    ).getTrackName(),
                    self.getSession(
                        self.getSessionIndex(columns[column_index])
                    ).getSessionName(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_track_room_penalties(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
            sheet_name="tracks_rooms|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__setTracksRoomsPenalty(
                    self.getTrack(
                        self.getTrackIndex(file.iloc[row_index, 0])
                    ).getTrackName(),
                    self.getRoom(
                        self.getRoomIndex(columns[column_index])
                    ).getRoomName(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_track_track_penalties(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
            sheet_name="similar tracks",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        penalty_list = file.values.tolist()

        for i in range(len(penalty_list)):
            for y in range(len(penalty_list)):
                if y != i:
                    self.__setTracksTracksPenalty(
                        self.getTrack(
                            self.getTrackIndex(penalty_list[i][0])
                        ).getTrackName(),
                        self.getTrack(
                            self.getTrackIndex(penalty_list[y][0])
                        ).getTrackName(),
                        penalty_list[y][i + 1],
                    )
                    self.__setTracksTracksPenalty(
                        self.getTrack(
                            self.getTrackIndex(penalty_list[y][0])
                        ).getTrackName(),
                        self.getTrack(
                            self.getTrackIndex(penalty_list[i][0])
                        ).getTrackName(),
                        penalty_list[y][i + 1],
                    )

    def __set_session_room_penalties(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
            sheet_name="sessions_rooms|penalty",
            keep_default_na=False,
            na_filter=False,
        )
        file.replace(to_replace="", value=0, inplace=True)
        columns = list(file.columns)
        columns.remove("Unnamed: 0")

        for row_index in range(len(file)):
            for column_index in range(len(columns)):
                self.__setSessionsRoomsPenalty(
                    self.getSession(
                        self.getSessionIndex(file.iloc[row_index, 0])
                    ).getSessionName(),
                    self.getRoom(
                        self.getRoomIndex(columns[column_index])
                    ).getRoomName(),
                    file.iloc[row_index, column_index + 1],
                )

    def __set_parameters(self) -> None:
        file = pd.read_excel(
            self.getFilePath(),
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
            num_rooms_per_track=int(file.iloc[4, 4][0]),
            parallel_tracks=int(file.iloc[5, 4][0]),
            consecutive_tracks=int(file.iloc[6, 4][0]),
            submissions_timezones_penalty_weight=int(file.iloc[7, 4][0]),
            submissions_order=int(file.iloc[8, 4][0]),
            submissions_sessions_penalty_weight=int(file.iloc[9, 4][0]),
            submissions_rooms_penalty_weight=int(file.iloc[10, 4][0]),
            presenters_conflicts=int(file.iloc[11, 4][0]),
            attendees_conflicts=int(file.iloc[12, 4][0]),
            chairs_conflicts=int(file.iloc[13, 4][0]),
            presenters_conflicts_timeslot_level=int(file.iloc[14, 4][0]),
            attendees_conflicts_timeslot_level=int(file.iloc[15, 4][0]),
            small_tz_penalty=int(file.iloc[7, 1][0]),
            big_tz_penalty=int(file.iloc[9, 1][0]),
        )

    def __setTrack(self, track: Track):
        self.__tracks.append(track)
        self.__tracks_map[track.getTrackName()] = len(self.__tracks_map)

    def __setSubmission(self, submission: Submission):
        self.__submissions.append(submission)
        self.__submissions_map[submission.getSubmissionName()] = len(
            self.__submissions_map
        )

    def __setSubmissionsSessionsPenalty(
        self, submission_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__submissions_sessions_penalty_map[submission_name + session_name] = (
            penalty_value
        )

    def __setSubmissionsTimezonesPenalty(
        self, submission_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__submissions_timezones_penalty_map[submission_name + session_name] = (
            penalty_value
        )

    def __setSubmissionsRoomsPenalty(
        self, submission_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__submissions_rooms_penalty_map[submission_name + room_name] = (
            penalty_value
        )

    def __setTracksSessionsPenalty(
        self, track_name: str, session_name: str, penalty_value: int
    ) -> None:
        self.__tracks_sessions_penalty_map[track_name + session_name] = penalty_value

    def __setTracksRoomsPenalty(
        self, track_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__tracks_rooms_penalty_map[track_name + room_name] = penalty_value

    def __setTracksTracksPenalty(
        self, this_track_name: str, other_track_name: str, penalty_value: int
    ) -> None:
        self.__tracks_tracks_penalty_map[this_track_name + other_track_name] = (
            penalty_value
        )

    def __setSessionsRoomsPenalty(
        self, session_name: str, room_name: str, penalty_value: int
    ) -> None:
        self.__sessions_rooms_penalty_map[session_name + room_name] = penalty_value

    def __check_feasibility_of_problem(self) -> None:
        if (
            self.getSumOfAvailableTimeSlots() * self.getNumberOfRooms()
            < self.getSumOfRequiredTimeSlots()
        ):
            raise ValueError(
                "Infeasible!: Not Enough Time Slots Available!\nConsider to add an extra session or room."
            )

    def __set_conflicts(self) -> None:
        for i in range(self.getNumberOfSubmissions()):
            for y in range(self.getNumberOfSubmissions()):
                if y != i:
                    for x in range(
                        len(self.getSubmission(i).getSubmissionAttendeesList())
                    ):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != "":
                            for z in range(
                                len(self.getSubmission(y).getSubmissionAttendeesList())
                            ):
                                if (
                                    self.getSubmission(i).getSubmissionAttendeesList()[
                                        x
                                    ]
                                    == self.getSubmission(
                                        y
                                    ).getSubmissionAttendeesList()[z]
                                ):
                                    self.getSubmission(
                                        i
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(y)
                                    )
                                    self.getSubmission(
                                        y
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(i)
                                    )
                    for x in range(
                        len(self.getSubmission(i).getSubmissionAttendeesList())
                    ):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != "":
                            for z in range(
                                len(self.getSubmission(y).getSubmissionPresentersList())
                            ):
                                if (
                                    self.getSubmission(i).getSubmissionAttendeesList()[
                                        x
                                    ]
                                    == self.getSubmission(
                                        y
                                    ).getSubmissionPresentersList()[z]
                                ):
                                    self.getSubmission(
                                        i
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(y)
                                    )
                                    self.getSubmission(
                                        y
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(i)
                                    )
                    for x in range(
                        len(self.getSubmission(i).getSubmissionAttendeesList())
                    ):
                        if self.getSubmission(i).getSubmissionAttendeesList()[x] != "":
                            for z in range(
                                len(
                                    self.getSubmission(y)
                                    .getSubmissionTrack()
                                    .getTrackChairsList()
                                )
                            ):
                                if (
                                    self.getSubmission(i).getSubmissionAttendeesList()[
                                        x
                                    ]
                                    == self.getSubmission(y)
                                    .getSubmissionTrack()
                                    .getTrackChairsList()[z]
                                ) and (
                                    self.getSubmission(i).getSubmissionTrack()
                                    != self.getSubmission(y).getSubmissionTrack()
                                ):
                                    self.getSubmission(
                                        i
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(y)
                                    )
                                    self.getSubmission(
                                        y
                                    ).setSubmissionAttendeeConflicts(
                                        self.getSubmission(i)
                                    )

    def __set_timezone_penalties(self) -> None:
        parameters = self.getParameters()
        suitable_from = dt.datetime(
            2021,
            7,
            21,
            int(parameters.getSuitableScheduleTimeFrom()[0]),
            int(parameters.getSuitableScheduleTimeFrom()[1]),
        ).time()
        suitable_to = dt.datetime(
            2021,
            7,
            21,
            int(parameters.getSuitableScheduleTimeTo()[0]),
            int(parameters.getSuitableScheduleTimeTo()[1]),
        ).time()
        less_suitable_from = dt.datetime(
            2021,
            7,
            21,
            int(parameters.getLessSuitableScheduleTimeFrom()[0]),
            int(parameters.getLessSuitableScheduleTimeFrom()[1]),
        ).time()
        less_suitable_to = dt.datetime(
            2021,
            7,
            21,
            int(parameters.getLessSuitableScheduleTimeTo()[0]),
            int(parameters.getLessSuitableScheduleTimeTo()[1]),
        ).time()
        for session_index in range(self.getNumberOfSessions()):
            # Defining session's local time zone
            loc_tz_st = (
                self.getSession(session_index)
                .getSessionStartTime()
                .replace(tzinfo=pytz.timezone(parameters.getLocalTimeZone()))
            )
            loc_tz_et = (
                self.getSession(session_index)
                .getSessionEndTime()
                .replace(tzinfo=pytz.timezone(parameters.getLocalTimeZone()))
            )
            for submission_index in range(self.getNumberOfSubmissions()):
                # Defining submission's time zone
                submission_tz = pytz.timezone(
                    self.getSubmission(submission_index).getSubmissionTimezone()
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
                    self.__setSubmissionsTimezonesPenalty(
                        self.getSubmission(submission_index).getSubmissionName(),
                        self.getSession(session_index).getSessionName(),
                        parameters.getBigTimeZonePenalty(),
                    )
                elif (
                    start_time >= less_suitable_from and start_time < suitable_from
                ) or (end_time > suitable_to and end_time <= less_suitable_to):
                    self.__setSubmissionsTimezonesPenalty(
                        self.getSubmission(submission_index).getSubmissionName(),
                        self.getSession(session_index).getSessionName(),
                        parameters.getSmallTimeZonePenalty(),
                    )
                else:
                    self.__setSubmissionsTimezonesPenalty(
                        self.getSubmission(submission_index).getSubmissionName(),
                        self.getSession(session_index).getSessionName(),
                        0,
                    )

    def __setSession(self, session: Session) -> None:
        self.__sessions.append(session)
        self.__sessions_map[session.getSessionName()] = len(self.__sessions_map)

    def __setRoom(self, room: Room) -> None:
        self.__rooms.append(room)
        self.__rooms_map[room.getRoomName()] = len(self.__rooms_map)

    def __check_all_sheets_exist(self) -> None:
        existing_sheets = self.__file.keys()
        for sheet in config.REQUIRED_SHEETS:
            if sheet not in existing_sheets:
                raise ValueError(f"Missing Sheet Error! \nMissing Sheet: {sheet}")

    def __check_for_duplicates(self) -> None:
        cols = list(
            pd.read_excel(
                self.getFilePath(), sheet_name="submissions", header=None, nrows=1
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
                    self.getFilePath(), sheet_name=sheet, header=None, nrows=1
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
        file = pd.read_excel(self.getFilePath(), None, header=None)
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
            != self.getNumberOfSessions() + self.getNumberOfRooms()
        ):
            raise ValueError(
                "Incorrect Number of Items Error! \nEnsure that number of sessions and rooms in sheet submissions match with number of itmes in sessions and rooms sheets."
            )

    def __check_naming_is_valid(self) -> None:
        for session_index in range(self.getNumberOfSessions()):
            if (
                self.getSession(session_index).getSessionName()
                not in self.__processed_submissions_file.columns[
                    config.COLUMNS_TO_INCLUDE : config.COLUMNS_TO_INCLUDE
                    + self.getNumberOfSessions()
                ]
            ):
                raise ValueError(
                    "Sessions Error!\nSessions names in submissions sheet must match those in sessions sheet."
                )

        for room_index in range(self.getNumberOfRooms()):
            if (
                self.getRoom(room_index).getRoomName()
                not in self.__processed_submissions_file.columns[
                    config.COLUMNS_TO_INCLUDE
                    + self.getNumberOfSessions() : config.COLUMNS_TO_INCLUDE
                    + self.getNumberOfSessions()
                    + self.getNumberOfRooms()
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

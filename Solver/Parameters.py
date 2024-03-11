# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

class Parameters:
    def __init__(self, local_time_zone, suitable_schedule_time_from, suitable_schedule_time_to,
                 less_suitable_schedule_time_from, less_suitable_schedule_time_to,
                 tracks_sessions_penalty_weight, tracks_rooms_penalty_weight, 
                 sessions_rooms_penalty_weight, similar_tracks_penalty_weight, 
                 num_rooms_per_track, parallel_tracks, consecutive_tracks, 
                 submissions_timezones_penalty_weight, submissions_order, 
                 submissions_sessions_penalty_weight, submissions_rooms_penalty_weight, 
                 presenters_conflicts, attendees_conflicts, chairs_conflicts,
                 presenters_conflicts_timeslot_level, attendees_conflicts_timeslot_level, small_tz_penalty, big_tz_penalty):
        self.__local_time_zone = local_time_zone
        self.__suitable_schedule_time_from = suitable_schedule_time_from
        self.__suitable_schedule_time_to = suitable_schedule_time_to
        self.__less_suitable_schedule_time_from = less_suitable_schedule_time_from
        self.__less_suitable_schedule_time_to = less_suitable_schedule_time_to
        self.__tracks_sessions_penalty_weight = tracks_sessions_penalty_weight
        self.__tracks_rooms_penalty_weight = tracks_rooms_penalty_weight
        self.__sessions_rooms_penalty_weight = sessions_rooms_penalty_weight
        self.__similar_tracks_penalty_weight = similar_tracks_penalty_weight
        self.__num_rooms_per_track = num_rooms_per_track
        self.__parallel_tracks = parallel_tracks
        self.__consecutive_tracks = consecutive_tracks
        self.__submissions_timezones_penalty_weight = submissions_timezones_penalty_weight
        self.__submissions_order = submissions_order
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
        self.__presenters_conflicts = presenters_conflicts
        self.__attendees_conflicts = attendees_conflicts
        self.__chairs_conflicts = chairs_conflicts
        self.__presenters_conflicts_timeslot_level = presenters_conflicts_timeslot_level
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level
        self.__small_tz_penalty = small_tz_penalty
        self.__big_tz_penalty = big_tz_penalty

    def getLocalTimeZone(self) -> str:
        return self.__local_time_zone
    def setLocalTimeZone(self, local_time_zone):
        self.__local_time_zone = local_time_zone
    def getSuitableScheduleTimeFrom(self):
        return self.__suitable_schedule_time_from
    def setSuitableScheduleTimeFrom(self, suitable_schedule_time_from):
        self.__suitable_schedule_time_from = suitable_schedule_time_from
    def getSuitableScheduleTimeTo(self):
        return self.__suitable_schedule_time_to
    def setSuitableScheduleTimeTo(self, suitable_schedule_time_to):
        self.__suitable_schedule_time_to = suitable_schedule_time_to
    def getLessSuitableScheduleTimeFrom(self):
        return self.__less_suitable_schedule_time_from
    def setLessSuitableScheduleTimeFrom(self, less_suitable_schedule_time_from):
        self.__less_suitable_schedule_time_from = less_suitable_schedule_time_from
    def getLessSuitableScheduleTimeTo(self):
        return self.__less_suitable_schedule_time_to
    def setLessSuitableScheduleTimeTo(self, less_suitable_schedule_time_to):
        self.__less_suitable_schedule_time_to = less_suitable_schedule_time_to
    def getTracksSessionsPenaltyWeight(self) -> int:
        return self.__tracks_sessions_penalty_weight
    def setTracksSessionsPenaltyWeight(self, tracks_sessions_penalty_weight):
        self.__tracks_sessions_penalty_weight = tracks_sessions_penalty_weight
    def getTracksRoomsPenaltyWeight(self) -> int:
        return self.__tracks_rooms_penalty_weight
    def setTracksRoomsPenaltyWeight(self, tracks_rooms_penalty_weight):
        self.__tracks_rooms_penalty_weight = tracks_rooms_penalty_weight
    def getSessionsRoomsPenaltyWeight(self) -> int:
        return self.__sessions_rooms_penalty_weight
    def setSessionsRoomsPenaltyWeight(self, sessions_rooms_penalty_weight):
        self.__sessions_rooms_penalty_weight = sessions_rooms_penalty_weight
    def getSimilarTracksPenaltyWeight(self) -> int:
        return self.__similar_tracks_penalty_weight
    def setSimilarTracksPenaltyWeight(self, similar_tracks_penalty_weight):
        self.__similar_tracks_penalty_weight = similar_tracks_penalty_weight
    def getNumOfRoomsPerTrackWeight(self) -> int:
        return self.__num_rooms_per_track
    def setNumOfRoomsPerTrackWeight(self, num_rooms_per_track):
        self.__num_rooms_per_track = num_rooms_per_track
    def getParallelTracksWeight(self) -> int:
        return self.__parallel_tracks
    def setParallelTracksWeight(self, parallel_tracks):
        self.__parallel_tracks = parallel_tracks
    def getConsecutiveTracksWeight(self) -> int:
        return self.__consecutive_tracks
    def setConsecutiveTracksWeight(self, consecutive_tracks):
        self._consecutive_tracks = consecutive_tracks
    def getSubmissionsTimezonesWeight(self) -> int:
        return self.__submissions_timezones_penalty_weight
    def setSubmissionsTimezonesPenaltyWeight(self, submissions_timezones_penalty_weight):
        self.__submissions_timezones_penalty_weight = submissions_timezones_penalty_weight
    def getSubmissionsOrderWeight(self) -> int:
        return self.__submissions_order
    def setSubmissionsOrderWeight(self, submissions_order):
        self.__submissions_order = submissions_order
    def getSubmissionsSessionsPenaltyWeight(self) -> int:
        return self.__submissions_sessions_penalty_weight
    def setSubmissionsSessionsWeight(self, submissions_sessions_penalty_weight):
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
    def getSubmissionsRoomsPenaltyWeight(self) -> int:
        return self.__submissions_rooms_penalty_weight
    def setSubmissionsRoomsPenaltyWeight(self, submissions_rooms_penalty_weight):
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
    def getPresentersConflictsWeight(self) -> int:
        return self.__presenters_conflicts
    def setPresentersConflictsWeight(self, presenters_conflicts):
        self.__presenters_conflicts = presenters_conflicts
    def getAteendeesConflictsWeight(self) -> int:
        return self.__attendees_conflicts
    def setAteendeesConflictsWeight(self, attendees_conflicts):
        self.__attendees_conflicts = attendees_conflicts
    def getChairsConflictsWeight(self) -> int:
        return self.__chairs_conflicts
    def setChairsConflictsWeight(self, chairs_conflicts):
        self.__chairs_conflicts = chairs_conflicts
    def getPresentersConflictsTimeslotLevelWeight(self) -> int:
        return self.__presenters_conflicts_timeslot_level
    def setPresentersConflictsTimeslotLevelWeight(self, presenters_conflicts_timeslot_level):
        self.__presenters_conflicts_timeslot_level = presenters_conflicts_timeslot_level
    def getAttendeesConflictsTimeSlotWeight(self) -> int:
        return self.__attendees_conflicts_timeslot_level
    def setAttendeesConflictsTimeSlotWeight(self, attendees_conflicts_timeslot_level):
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level
    def getSmallTimeZonePenalty(self) -> int:
        return self.__small_tz_penalty
    def setSmallTimeZonePenalty(self, small_tz_penalty):
        self.__small_tz_penalty = small_tz_penalty
    def getBigTimeZonePenalty(self):
        return self.__big_tz_penalty
    def setBigTimeZonePenalty(self, big_tz_penalty):
        self.__big_tz_penalty = big_tz_penalty
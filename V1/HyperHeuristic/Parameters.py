# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:18:28 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

class Parameters:
    def __init__(self, local_time_zone, schedule_time_from, schedule_time_to, 
                 tracks_sessions_penalty_weight, tracks_rooms_penalty_weight, 
                 sessions_rooms_penalty_weight, tracks_tracks_penalty_weight, 
                 num_rooms_per_track, parallel_tracks, consecutive_tracks, 
                 tracks_relative_order, submissions_timezones_penalty_weight, 
                 submissions_relative_order, submissions_actual_order, submissions_sessions_penalty_weight, 
                 submissions_rooms_penalty_weight, speakers_conflicts, 
                 attendees_conflicts, organiser_conflicts, 
                 tracks_buildings, balance, speakers_conflicts_timeslot_level, 
                 attendees_conflicts_timeslot_level, open_session_weight, 
                 close_session_weight, same_session_weight, different_session_weight,
                 track_max_num_days_weight, tracks_same_room_weight, tracks_same_building_weight,
                 preferred_num_time_slots):
        self.__local_time_zone = local_time_zone
        self.__schedule_time_from = schedule_time_from
        self.__schedule_time_to = schedule_time_to
        self.__tracks_sessions_penalty_weight = tracks_sessions_penalty_weight
        self.__tracks_rooms_penalty_weight = tracks_rooms_penalty_weight
        self.__sessions_rooms_penalty_weight = sessions_rooms_penalty_weight
        self.__tracks_tracks_penalty_weight = tracks_tracks_penalty_weight
        self.__num_rooms_per_track = num_rooms_per_track
        self.__parallel_tracks = parallel_tracks
        self.__consecutive_tracks = consecutive_tracks
        self.__tracks_relative_order = tracks_relative_order
        self.__submissions_timezones_penalty_weight = submissions_timezones_penalty_weight
        self.__submissions_relative_order = submissions_relative_order
        self.__submissions_actual_order = submissions_actual_order
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
        self.__speakers_conflicts = speakers_conflicts
        self.__attendees_conflicts = attendees_conflicts
        self.__organiser_conflicts = organiser_conflicts
        self.__tracks_buildings = tracks_buildings
        self.__balance = balance
        self.__speakers_conflicts_timeslot_level = speakers_conflicts_timeslot_level
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level
        self.__open_session_weight = open_session_weight
        self.__close_session_weight = close_session_weight
        self.__same_session_weight = same_session_weight
        self.__different_session_weight = different_session_weight
        self.__track_max_num_days_weight = track_max_num_days_weight
        self.__tracks_same_room_weight = tracks_same_room_weight
        self.__tracks_same_building_weight = tracks_same_building_weight
        self.__preferred_num_time_slots = preferred_num_time_slots

    def getLocalTimeZone(self) -> str:
        return self.__local_time_zone
    def setLocalTimeZone(self, local_time_zone):
        self.__local_time_zone = local_time_zone
    def getScheduleTimeFrom(self):
        return self.__schedule_time_from
    def setScheduleTimeFrom(self, schedule_time_from):
        self.__schedule_time_from = schedule_time_from
    def getScheduleTimeTo(self):
        return self.__schedule_time_to
    def setScheduleTimeTo(self, schedule_time_to):
        self.__schedule_time_to = schedule_time_to
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
    def getTracksTracksPenaltyWeight(self) -> int:
        return self.__tracks_tracks_penalty_weight
    def setTracksTracksPenaltyWeight(self, tracks_tracks_penalty_weight):
        self.__tracks_tracks_penalty_weight = tracks_tracks_penalty_weight
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
    def getTracksRelativeOrderWeight(self) -> int:
        return self.__tracks_relative_order
    def setTracksRelativeOrderWeight(self, tracks_relative_order):
        self.__tracks_relative_order = tracks_relative_order
    def getSubmissionsTimezonesWeight(self) -> int:
        return self.__submissions_timezones_penalty_weight
    def setSubmissionsTimezonesPenaltyWeight(self, submissions_timezones_penalty_weight):
        self.__submissions_timezones_penalty_weight = submissions_timezones_penalty_weight
    def getSubmissionsRelativeOrderWeight(self) -> int:
        return self.__submissions_relative_order
    def setSubmissionsRelativeOrderWeight(self, submissions_relative_order):
        self.__submissions_relative_order = submissions_relative_order
    def getSubmissionsActualOrderWeight(self) -> int:
        return self.__submissions_actual_order
    def setSubmissionsActualOrderWeight(self, submissions_actual_order):
        self.__submissions_actual_order = submissions_actual_order
    def getSubmissionsSessionsPenaltyWeight(self) -> int:
        return self.__submissions_sessions_penalty_weight
    def setSubmissionsSessionsWeight(self, submissions_sessions_penalty_weight):
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
    def getSubmissionsRoomsPenaltyWeight(self) -> int:
        return self.__submissions_rooms_penalty_weight
    def setSubmissionsRoomsPenaltyWeight(self, submissions_rooms_penalty_weight):
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
    def getSpeakersConflictsWeight(self) -> int:
        return self.__speakers_conflicts
    def setSpeakersConflictsWeight(self, speakers_conflicts):
        self.__speakers_conflicts = speakers_conflicts
    def getAteendeesConflictsWeight(self) -> int:
        return self.__attendees_conflicts
    def setAteendeesConflictsWeight(self, attendees_conflicts):
        self.__attendees_conflicts = attendees_conflicts
    def getOrganisersConflictsWeight(self) -> int:
        return self.__organiser_conflicts
    def setOrganisersConflictsWeight(self, organiser_conflicts):
        self.__organiser_conflicts = organiser_conflicts
    def getTracksBuildingsWeight(self) -> int:
        return self.__tracks_buildings
    def setTracksBuildingsWeight(self, tracks_buildings):
        self.__tracks_buildings = tracks_buildings
    def getBalanceWeight(self) -> int:
        return self.__balance
    def setBalanceWeight(self, balance):
        self.__balance = balance
    def getSpeakersConflictsTimeslotLevelWeight(self) -> int:
        return self.__speakers_conflicts_timeslot_level
    def setSpeakersConflictsTimeslotLevelWeight(self, speakers_conflicts_timeslot_level):
        self.__speakers_conflicts_timeslot_level = speakers_conflicts_timeslot_level
    def getAttendeesConflictsTimeSlotWeight(self) -> int:
        return self.__attendees_conflicts_timeslot_level
    def setAttendeesConflictsTimeSlotWeight(self, attendees_conflicts_timeslot_level):
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level   
    def getOpenSessionWeight(self) -> int:
        return self.__open_session_weight
    def setOpenSessionWeight(self, open_session_weight):
        self.__open_session_weight = open_session_weight   
    def getCloseSessionWeight(self) -> int:
        return self.__close_session_weight
    def setCloseSessionWeight(self, close_session_weight):
        self.__close_session_weight = close_session_weight  
    def getSameSessionWeight(self) -> int:
        return self.__same_session_weight
    def setSameSessionWeight(self, same_session_weight):
        self.__same_session_weight = same_session_weight    
    def getDifferentSessionWeight(self) -> int:
        return self.__different_session_weight
    def setDifferentSessionWeight(self, different_session_weight):
        self.__different_session_weight = different_session_weight
    def getTrackMaxNumDaysWeight(self) -> int:
        return self.__track_max_num_days_weight
    def setTrackMaxNumDaysWeight(self, track_max_num_days_weight):
        self.__track_max_num_days_weight = track_max_num_days_weight   
    def getTrackSameRoomWeight(self) -> int:
        return self.__tracks_same_room_weight
    def setTrackSameRoomWeight(self, tracks_same_room_weight):
        self.__tracks_same_room_weight = tracks_same_room_weight
    def getTracksSameBuildingWeight(self) -> int:
        return self.__tracks_same_building_weight
    def setTracksSameBuildingWeight(self, tracks_same_building_weight):
        self.__tracks_same_building_weight = tracks_same_building_weight   
    def getPreferredNumTimeSlotsWeight(self) -> int:
        return self.__preferred_num_time_slots
    def setPreferredNumTimeSlotsWeight(self, preferred_num_time_slots):
        self.__preferred_num_time_slots = preferred_num_time_slots  
        
if __name__ == '__main__':
    parameters = Parameters('GMT+2', '9:00', '21:00', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
                            , 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    print(parameters.getLocalTimeZone())
    parameters.setLocalTimeZone('GMT+3')
    print(parameters.getLocalTimeZone())
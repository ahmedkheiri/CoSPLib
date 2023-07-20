# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:18:28 2023

@author: pylya
"""

class Parameters:
    def __init__(self, tracks_sessions_penalty_weight, tracks_rooms_penalty_weight, 
                 sessions_rooms_penalty_weight, tracks_tracks_penalty_weight, 
                 num_rooms_per_track, parallel_tracks, consecutive_tracks, 
                 tracks_relative_order, tracks_actual_order, 
                 submissions_timezones_penalty_weight, submissions_relative_order, 
                 submissions_actual_order, submissions_sessions_penalty_weight, 
                 submissions_rooms_penalty_weight, speakers_conflicts, 
                 attendees_conflicts, organiser_conflicts, track_duration, 
                 tracks_buildings, balance, speakers_conflicts_timeslot_level, 
                 attendees_conflicts_timeslot_level, open_session_weight, 
                 close_session_weight, same_session_weight, different_session_weight,
                 track_max_num_days_weight, tracks_same_room_weight, tracks_same_building_weight,
                 preferred_num_time_slots, min_num_time_slots, max_num_time_slots):
        self.__tracks_sessions_penalty_weight = tracks_sessions_penalty_weight
        self.__tracks_rooms_penalty_weight = tracks_rooms_penalty_weight
        self.__sessions_rooms_penalty_weight = sessions_rooms_penalty_weight
        self.__tracks_tracks_penalty_weight = tracks_tracks_penalty_weight
        self.__num_rooms_per_track = num_rooms_per_track
        self.__parallel_tracks = parallel_tracks
        self.__consecutive_tracks = consecutive_tracks
        self.__tracks_relative_order = tracks_relative_order
        self.__tracks_actual_order = tracks_actual_order
        self.__submissions_timezones_pnealty_weight = submissions_timezones_penalty_weight
        self.__submissions_relative_order = submissions_relative_order
        self.__submissions_actual_order = submissions_actual_order
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
        self.__speakers_conflicts = speakers_conflicts
        self.__attendees_conflicts = attendees_conflicts
        self.__organiser_conflicts = organiser_conflicts
        self.__track_duration = track_duration
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
        self.__min_num_time_slots = min_num_time_slots
        self.__max_num_time_slots = max_num_time_slots

    
    def getTracksSessionsPenaltyWeight(self):
        return self.__tracks_sessions_penalty_weight

    def setTracksSessionsPenaltyWeight(self, tracks_sessions_penalty_weight):
        self.__tracks_sessions_penalty_weight = tracks_sessions_penalty_weight

    def getTracksRoomsPenaltyWeight(self):
        return self.__tracks_rooms_penalty_weight

    def setTracksRoomsPenaltyWeight(self, tracks_rooms_penalty_weight):
        self.__tracks_rooms_penalty_weight = tracks_rooms_penalty_weight

    def getSessionsRoomsPenaltyWeight(self):
        return self.__sessions_rooms_penalty_weight

    def setSessionsRoomsPenaltyWeight(self, sessions_rooms_penalty_weight):
        self.__sessions_rooms_penalty_weight = sessions_rooms_penalty_weight

    def getTracksTracksPenaltyWeight(self):
        return self.__tracks_tracks_penalty_weight

    def setTracksTracksPenaltyWeight(self, tracks_tracks_penalty_weight):
        self.__tracks_tracks_penalty_weight = tracks_tracks_penalty_weight

    def getNumOfRoomsPerTrackWeight(self):
        return self.__num_rooms_per_track

    def setNumOfRoomsPerTrackWeight(self, num_rooms_per_track):
        self.__num_rooms_per_track = num_rooms_per_track

    def getParallelTracksWeight(self):
        return self.__parallel_tracks

    def setParallelTracksWeight(self, parallel_tracks):
        self.__parallel_tracks = parallel_tracks

    def getConsecutiveTracksWeight(self):
        return self.__consecutive_tracks

    def setConsecutiveTracksWeight(self, consecutive_tracks):
        self._consecutive_tracks = consecutive_tracks

    def getTracksRelativeOrderWeight(self):
        return self.__tracks_relative_order

    def setTracksRelativeOrderWeight(self, tracks_relative_order):
        self.__tracks_relative_order = tracks_relative_order

    def getTracksActualOrderWeight(self):
        return self.__tracks_actual_order

    def setTracksActualOrderWeight(self, tracks_actual_order):
        self.__tracks_actual_order = tracks_actual_order

    def getSubmissionsTimezonesWeight(self):
        return self.__submissions_timezones_penalty_weight

    def setSubmissionsTimezonesPenaltyWeight(self, submissions_timezones_penalty_weight):
        self.__submissions_timezones_penalty_weight = submissions_timezones_penalty_weight

    def getSubmissionsRelativeOrderWeight(self):
        return self.__submissions_relative_order

    def setSubmissionsRelativeOrderWeight(self, submissions_relative_order):
        self.__submissions_relative_order = submissions_relative_order

    def getSubmissionsActualOrderWeight(self):
        return self.__submissions_actual_order

    def setSubmissionsActualOrderWeight(self, submissions_actual_order):
        self.__submissions_actual_order = submissions_actual_order

    def getSubmissionsSessionsPenaltyWeight(self):
        return self.__submissions_sessions_penalty_weight

    def setSubmissionsSessionsWeight(self, submissions_sessions_penalty_weight):
        self.__submissions_sessions_penalty_weight = submissions_sessions_penalty_weight

    def getSubmissionsRoomsPenaltyWeight(self):
        return self.__submissions_rooms_penalty_weight

    def setSubmissionsRoomsPenaltyWeight(self, submissions_rooms_penalty_weight):
        self.__submissions_rooms_penalty_weight = submissions_rooms_penalty_weight

    def getSpeakersConflictsWeight(self):
        return self.__speakers_conflicts

    def setSpeakersConflictsWeight(self, speakers_conflicts):
        self.__speakers_conflicts = speakers_conflicts

    def getAteendeesConflictsWeight(self):
        return self.__attendees_conflicts

    def setAteendeesConflictsWeight(self, attendees_conflicts):
        self.__attendees_conflicts = attendees_conflicts

    def getOrganisersConflictsWeight(self):
        return self.__organiser_conflicts

    def setOrganisersConflictsWeight(self, organiser_conflicts):
        self.__organiser_conflicts = organiser_conflicts

    def getTrackDurationWeight(self):
        return self.__track_duration

    def setTrackDurationWeight(self, track_duration):
        self.__track_duration = track_duration

    def getTracksBuildingsWeight(self):
        return self.__tracks_buildings

    def setTracksBuildingsWeight(self, tracks_buildings):
        self.__tracks_buildings = tracks_buildings

    def getBalanceWeight(self):
        return self.__balance

    def setBalanceWeight(self, balance):
        self.__balance = balance

    def getSpeakersConflictsTimeslotLevelWeight(self):
        return self.__speakers_conflicts_timeslot_level

    def setSpeakersConflictsTimeslotLevelWeight(self, speakers_conflicts_timeslot_level):
        self.__speakers_conflicts_timeslot_level = speakers_conflicts_timeslot_level

    def getAttendeesConflictsTimeSlotWeight(self):
        return self.__attendees_conflicts_timeslot_level

    def setAttendeesConflictsTimeSlotWeight(self, attendees_conflicts_timeslot_level):
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level
        
    def getOpenSessionWeight(self):
        return self.__open_session_weight
    
    def setOpenSessionWeight(self, open_session_weight):
        self.__open_session_weight = open_session_weight
        
    def getCloseSessionWeight(self):
        return self.__close_session_weight
    
    def setCloseSessionWeight(self, close_session_weight):
        self.__close_session_weight = close_session_weight
        
    def getSameSessionWeight(self):
        return self.__same_session_weight
    
    def setSameSessionWeight(self, same_session_weight):
        self.__same_session_weight = same_session_weight
        
    def getDifferentSessionWeight(self):
        return self.__different_session_weight
    
    def setDifferentSessionWeight(self, different_session_weight):
        self.__different_session_weight = different_session_weight
    
    def getTrackMaxNumDaysWeight(self):
        return self.__track_max_num_days_weight
    
    def setTrackMaxNumDaysWeight(self, track_max_num_days_weight):
        self.__track_max_num_days_weight = track_max_num_days_weight
        
    def getTrackSameRoomWeight(self):
        return self.__tracks_same_room_weight
    
    def setTrackSameRoomWeight(self, tracks_same_room_weight):
        self.__tracks_same_room_weight = tracks_same_room_weight
    
    def getTracksSameBuildingWeight(self):
        return self.__tracks_same_building_weight
    
    def setTracksSameBuildingWeight(self, tracks_same_building_weight):
        self.__tracks_same_building_weight = tracks_same_building_weight
        
    def getPreferredNumTimeSlotsWeight(self):
        return self.__preferred_num_time_slots
    
    def setPreferredNumTimeSlotsWeight(self, preferred_num_time_slots):
        self.__preferred_num_time_slots = preferred_num_time_slots
        
    def getMinNumTimeSlotsWeight(self):
        return self.__min_num_time_slots
    
    def setMinNumTimeSlotsWeight(self, min_num_time_slots):
        self.__min_num_time_slots = min_num_time_slots
    
    def getMaxNumTimeSlotsWeight(self):
        return self.__max_num_time_slots
    
    def setMaxNumTimeSlotsWeight(self, max_num_time_slots):
        self.__max_num_time_slots = max_num_time_slots
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 20 15:18:28 2023

@author: pylya
"""

class Parameters:
    def __init__(self, tracks_sessions_penalty, tracks_rooms_penalty, sessions_rooms_penalty, tracks_tracks_penalty, 
                 num_rooms_per_track, parallel_tracks, consecutive_tracks, tracks_relative_order, tracks_actual_order, 
                 submissions_timezones_penalty, submissions_relative_order, submissions_actual_order, submissions_sessions_penalty, 
                 submissions_rooms_penalty, speakers_conflicts, attendees_conflicts, organiser_conflicts, track_duration, 
                 tracks_buildings, balance, speakers_conflicts_timeslot_level, attendees_conflicts_timeslot_level):
        self.__tracks_sessions_penalty = tracks_sessions_penalty
        self.__tracks_rooms_penalty = tracks_rooms_penalty
        self.__sessions_rooms_penalty = sessions_rooms_penalty
        self.__tracks_tracks_penalty = tracks_tracks_penalty
        self.__num_rooms_per_track = num_rooms_per_track
        self.__parallel_tracks = parallel_tracks
        self.__consecutive_tracks = consecutive_tracks
        self.__tracks_relative_order = tracks_relative_order
        self.__tracks_actual_order = tracks_actual_order
        self.__submissions_timezones_penalty = submissions_timezones_penalty
        self.__submissions_relative_order = submissions_relative_order
        self.__submissions_actual_order = submissions_actual_order
        self.__submissions_sessions_penalty = submissions_sessions_penalty
        self.__submissions_rooms_penalty = submissions_rooms_penalty
        self.__speakers_conflicts = speakers_conflicts
        self.__attendees_conflicts = attendees_conflicts
        self.__organiser_conflicts = organiser_conflicts
        self.__track_duration = track_duration
        self.__tracks_buildings = tracks_buildings
        self.__balance = balance
        self.__speakers_conflicts_timeslot_level = speakers_conflicts_timeslot_level
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level

    
    def getTracksSessionsPenalty(self):
        return self.__tracks_sessions_penalty

    def setTracksSessionsPenalty(self, tracks_sessions_penalty):
        self.__tracks_sessions_penalty = tracks_sessions_penalty

    def getTracksRoomsPenalty(self):
        return self.__tracks_rooms_penalty

    def setTracksRoomsPenalty(self, tracks_rooms_penalty):
        self.__tracks_rooms_penalty = tracks_rooms_penalty

    def getSessionsRoomsPenalty(self):
        return self.__sessions_rooms_penalty

    def setSessionsRoomsPenalty(self, sessions_rooms_penalty):
        self.__sessions_rooms_penalty = sessions_rooms_penalty

    def getTracksTracksPenalty(self):
        return self.__tracks_tracks_penalty

    def setTracksTracksPenalty(self, tracks_tracks_penalty):
        self.__tracks_tracks_penalty = tracks_tracks_penalty

    def getNumOfRoomsPerTrackPenalty(self):
        return self.__num_rooms_per_track

    def setNumOfRoomsPerTrackPenalty(self, num_rooms_per_track):
        self.__num_rooms_per_track = num_rooms_per_track

    def getParallelTracksPenalty(self):
        return self.__parallel_tracks

    def setParallelTracksPenalty(self, parallel_tracks):
        self.__parallel_tracks = parallel_tracks

    def getConsecutiveTracksPenalty(self):
        return self.__consecutive_tracks

    def setConsecutiveTracksPenalty(self, consecutive_tracks):
        self._consecutive_tracks = consecutive_tracks

    def getTracksRelativeOrderPenalty(self):
        return self.__tracks_relative_order

    def setTracksRelativeOrderPenalty(self, tracks_relative_order):
        self.__tracks_relative_order = tracks_relative_order

    def getTracksActualOrderPenalty(self):
        return self.__tracks_actual_order

    def setTracksActualOrderPenalty(self, tracks_actual_order):
        self.__tracks_actual_order = tracks_actual_order

    def getSubmissionsTimezonesPenalty(self):
        return self.__submissions_timezones_penalty

    def setSubmissionsTimezonesPenalty(self, submissions_timezones_penalty):
        self.__submissions_timezones_penalty = submissions_timezones_penalty

    def getSubmissionsRelativeOrderPenalty(self):
        return self.__submissions_relative_order

    def setSubmissionsRelativeOrderPenalty(self, submissions_relative_order):
        self.__submissions_relative_order = submissions_relative_order

    def getSubmissionsActualOrder(self):
        return self.__submissions_actual_order

    def setSubmissionsActualOrder(self, submissions_actual_order):
        self.__submissions_actual_order = submissions_actual_order

    def getSubmissionsSessionsPenalty(self):
        return self.__submissions_sessions_penalty

    def setSubmissionsSessionsPenalty(self, submissions_sessions_penalty):
        self.__submissions_sessions_penalty = submissions_sessions_penalty

    def getSubmissionsRoomsPenalty(self):
        return self.__submissions_rooms_penalty

    def setSubmissionsRoomsPenalty(self, submissions_rooms_penalty):
        self.__submissions_rooms_penalty = submissions_rooms_penalty

    def getSpeakersConflictsPenalty(self):
        return self.__speakers_conflicts

    def setSpeakersConflictsPenalty(self, speakers_conflicts):
        self.__speakers_conflicts = speakers_conflicts

    def getAteendeesConflictsPenalty(self):
        return self.__attendees_conflicts

    def setAteendeesConflictsPenalty(self, attendees_conflicts):
        self.__attendees_conflicts = attendees_conflicts

    def getOrganisersConflicts(self):
        return self.__organiser_conflicts

    def setOrganisersConflicts(self, organiser_conflicts):
        self.__organiser_conflicts = organiser_conflicts

    def getTrackDurationPenalty(self):
        return self.__track_duration

    def setTrackDurationPenalty(self, track_duration):
        self.__track_duration = track_duration

    def getTracksBuildingsPenalty(self):
        return self.__tracks_buildings

    def setTracksBuildingsPenalty(self, tracks_buildings):
        self.__tracks_buildings = tracks_buildings

    def getBalancePenalty(self):
        return self.__balance

    def setBalancePenalty(self, balance):
        self.__balance = balance

    def getSpeakersConflictsTimeslotLevelPenalty(self):
        return self.__speakers_conflicts_timeslot_level

    def setSpeakersConflictsTimeslotLevelPenalty(self, speakers_conflicts_timeslot_level):
        self.__speakers_conflicts_timeslot_level = speakers_conflicts_timeslot_level

    def getAttendeesConflictsTimeSlotPenalty(self):
        return self.__attendees_conflicts_timeslot_level

    def setAttendeesConflictsTimeSlotPenalty(self, attendees_conflicts_timeslot_level):
        self.__attendees_conflicts_timeslot_level = attendees_conflicts_timeslot_level
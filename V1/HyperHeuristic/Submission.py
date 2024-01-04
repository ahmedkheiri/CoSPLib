# -*- coding: utf-8 -*-
"""
Created on Wed Jun 14 15:23:01 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)

"""

import Participant
import Track
class Submission:
    def __init__(self, name, track, required_time_slots, rel_order, act_order, can_open_session, can_close_session, same_session, different_session, speakers, attendees, speaker_conflicts, attendee_conflicts):        
        self.__name = name
        self.__track = track
        self.__required_time_slots = required_time_slots
        self.__rel_order = rel_order
        self.__act_order = act_order
        self.__can_open_session = can_open_session
        self.__can_close_session = can_close_session
        self.__same_session = same_session
        self.__different_session = different_session
        self.__speakers = speakers
        self.__attendees = attendees
        self.__speaker_conflicts = speaker_conflicts
        self.__attendee_conflicts = attendee_conflicts
    def getSubmissionName(self) -> str:
        return self.__name
    def setSubmissionName(self, name):
        self.__name = name
    def getSubmissionTrack(self) -> Track:
        return self.__track
    def setSubmissionTrack(self, track):
        self.__track = track
    def getSubmissionRequiredTimeSlots(self) -> int:
        return self.__required_time_slots
    def setSubmissionRequiredTimeSlots(self, required_time_slots):
        self.__required_time_slots = required_time_slots
    def getSubmissionRelativeOrder(self) -> int:
        return self.__rel_order
    def setSubmissionRelativeOrder(self, rel_order):
        self.__rel_order = rel_order
    def getSubmissionActualOrder(self) -> int:
        return self.__act_order
    def setSubmissionActualOrder(self, act_order):
        self.__act_order = act_order
    def getSubmissionCanOpenSession(self) -> bool:
        return self.__can_open_session
    def setSubmissionCanOpenSession(self, can_open_session):
        self.__can_open_session = can_open_session
    def getSubmissionCanCloseSession(self) -> bool:
        return self.__can_close_session
    def setSubmissionCanCloseSession(self, can_close_session):
        self.__can_close_session = can_close_session
    def getNumberOfSubmissionSameSession(self) -> int:
        return len(self.__same_session)
    def getSubmissionSameSession(self, same_session_index) -> 'Submission':
        return self.__same_session[same_session_index]
    def getSubmissionSameSessionList(self) -> list:
        return self.__same_session
    def setSubmissionSameSession(self, submission):
        self.__same_session.append(submission)
    def setSubmissionSameSessionList(self, same_session_list):
        self.__same_session = same_session_list
    def getNumberOfSubmissionDifferentSession(self) -> int:
        return len(self.__different_session)
    def getSubmissionDifferentSession(self, different_session_index) -> 'Submission':
        return self.__different_session[different_session_index]
    def getSubmissionDifferentSessionList(self) -> list:
        return self.__different_session
    def setSubmissionDifferentSession(self, submission):
        self.__different_session.append(submission)
    def setSubmissionDifferentSessionList(self, different_session_list):
        self.__different_session = different_session_list
    def getNumberOfSubmissionSpeakers(self) -> int:
        return len(self.__speakers)
    def getSubmissionSpeakers(self, speakers_index) -> Participant:
        return self.__speakers[speakers_index]
    def getSubmissionSpeakersList(self) -> list:
        return self.__speakers
    def setSubmissionSpeakers(self, participant):
        self.__speakers.append(participant)
    def setSubmissionSpeakersList(self, speakers_list):
        self.__speakers = speakers_list
    def getNumberOfSubmissionAttendees(self) -> int:
        return len(self.__attendees)
    def getSubmissionAttendees(self, attendees_index) -> Participant:
        return self.__attendees[attendees_index]
    def getSubmissionAttendeesList(self) -> list:
        return self.__attendees
    def setSubmissionAttendees(self, participant):
        self.__attendees.append(participant)
    def setSubmissionAttendeesList(self, attendees_list):
        self.__attendees = attendees_list
    def getNumberOfSubmissionSpeakerConflicts(self) -> int:
        return len(self.__speaker_conflicts)
    def getSubmissionSpeakerConflicts(self, speaker_conflict_index) -> Participant:
        return self.__speaker_conflicts[speaker_conflict_index]
    def getSubmissionSpeakerConflictsList(self) -> list:
        return self.__speaker_conflicts
    def setSubmissionSpeakerConflicts(self, submission):
        if submission not in self.__speaker_conflicts:
            self.__speaker_conflicts.append(submission)
    def getNumberOfSubmissionAttendeeConflicts(self) -> int:
        return len(self.__attendee_conflicts)
    def getSubmissionAttendeeConflicts(self, attendee_conflict_index) -> Participant:
        return self.__attendee_conflicts[attendee_conflict_index]
    def getSubmissionAttendeeConflictsList(self) -> list:
        return self.__attendee_conflicts
    def setSubmissionAttendeeConflicts(self, submission):
        if submission not in self.__attendee_conflicts:
            self.__attendee_conflicts.append(submission)
        
    def __str__(self):
        return "Submission("+self.__name+")"
        
if __name__ == '__main__':
    sub = Submission('NEWSubmission', Track.Track('NEWTrack', 0, 0, 0, 0, [], [], [], [], []), 1, 0, 0, True, True, [], [], [], [], [], [])
    print(sub.getSubmissionName())
    sub.setSubmissionName('Submission_1')
    print(sub)
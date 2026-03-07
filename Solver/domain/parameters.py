# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 19:16:16 2023

@authors: Yaroslav Pylyavskyy (pylyavskyy@hotmail.com) & Ahmed Kheiri (a.o.kheiri@gmail.com)
"""

from dataclasses import dataclass


@dataclass
class Parameters:
    def __init__(
        self,
        local_time_zone: str,
        suitable_schedule_time_from: str,
        suitable_schedule_time_to: str,
        less_suitable_schedule_time_from: str,
        less_suitable_schedule_time_to: str,
        tracks_sessions_penalty_weight: int,
        tracks_rooms_penalty_weight: int,
        sessions_rooms_penalty_weight: int,
        similar_tracks_penalty_weight: int,
        num_rooms_per_track_weight: int,
        parallel_tracks_weight: int,
        consecutive_tracks_weight: int,
        submissions_timezones_penalty_weight: int,
        submissions_order_weight: int,
        submissions_sessions_penalty_weight: int,
        submissions_rooms_penalty_weight: int,
        presenters_conflicts_weight: int,
        attendees_conflicts_weight: int,
        chairs_conflicts_weight: int,
        presenters_conflicts_timeslot_level_weight: int,
        attendees_conflicts_timeslot_level_weight: int,
        small_timezone_penalty: int,
        big_timezone_penalty: int,
    ):
        self.local_time_zone = local_time_zone
        self.suitable_schedule_time_from = suitable_schedule_time_from
        self.suitable_schedule_time_to = suitable_schedule_time_to
        self.less_suitable_schedule_time_from = less_suitable_schedule_time_from
        self.less_suitable_schedule_time_to = less_suitable_schedule_time_to
        self.tracks_sessions_penalty_weight = tracks_sessions_penalty_weight
        self.tracks_rooms_penalty_weight = tracks_rooms_penalty_weight
        self.sessions_rooms_penalty_weight = sessions_rooms_penalty_weight
        self.similar_tracks_penalty_weight = similar_tracks_penalty_weight
        self.num_rooms_per_track_weight = num_rooms_per_track_weight
        self.parallel_tracks_weight = parallel_tracks_weight
        self.consecutive_tracks_weight = consecutive_tracks_weight
        self.submissions_timezones_penalty_weight = submissions_timezones_penalty_weight
        self.submissions_order_weight = submissions_order_weight
        self.submissions_sessions_penalty_weight = submissions_sessions_penalty_weight
        self.submissions_rooms_penalty_weight = submissions_rooms_penalty_weight
        self.presenters_conflicts_weight = presenters_conflicts_weight
        self.attendees_conflicts_weight = attendees_conflicts_weight
        self.chairs_conflicts_weight = chairs_conflicts_weight
        self.presenters_conflicts_timeslot_level_weight = (
            presenters_conflicts_timeslot_level_weight
        )
        self.attendees_conflicts_timeslot_level_weight = (
            attendees_conflicts_timeslot_level_weight
        )
        self.small_timezone_penalty = small_timezone_penalty
        self.big_timezone_penalty = big_timezone_penalty

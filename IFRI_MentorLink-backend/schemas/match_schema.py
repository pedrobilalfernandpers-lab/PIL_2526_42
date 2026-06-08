# schemas/match_schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MatchUserInfo(BaseModel):
    """Infos minimales sur un utilisateur affichées dans un match"""
    id:            int
    first_name:    str
    last_name:     str
    profile_photo: Optional[str]
    field_of_study: str
    level:         str

    class Config:
        from_attributes = True


class CommonAvailability(BaseModel):
    """Un créneau commun entre mentor et mentoré"""
    day_of_week: str
    start_time:  str
    end_time:    str


class MatchResponse(BaseModel):
    """Un match tel que renvoyé par GET /api/matches"""
    id:                   int
    mentor:               MatchUserInfo
    mentee:               MatchUserInfo
    skill_id:             Optional[int]
    skill_name:           Optional[str]
    score:                float
    status:               str    # 'pending', 'accepted', 'rejected'
    common_availabilities: List[CommonAvailability] = []
    created_at:           datetime

    class Config:
        from_attributes = True
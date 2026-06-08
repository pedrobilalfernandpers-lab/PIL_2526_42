# schemas/user_schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time


class SkillInProfile(BaseModel):
    """Une compétence telle qu'elle apparaît dans le profil"""
    skill_id:    int
    skill_name:  str
    proficiency: str   # 'strong' ou 'weak'

    class Config:
        from_attributes = True  # permet de convertir un objet SQLAlchemy en schéma


class AvailabilityInProfile(BaseModel):
    """Un créneau de disponibilité dans le profil"""
    id:          int
    day_of_week: str
    start_time:  time
    end_time:    time

    class Config:
        from_attributes = True


class UserProfileResponse(BaseModel):
    """Profil complet renvoyé par GET /api/users/me"""
    id:            int
    first_name:    str
    last_name:     str
    email:         str
    phone_number:  str
    profile_photo: Optional[str]
    field_of_study: str
    level:         str
    bio:           Optional[str]
    skills:        List[SkillInProfile]       = []
    availabilities: List[AvailabilityInProfile] = []
    created_at:    datetime

    class Config:
        from_attributes = True


class UpdateProfileRequest(BaseModel):
    """Données envoyées par PUT /api/users/me — tous les champs sont optionnels"""
    first_name:    Optional[str] = None
    last_name:     Optional[str] = None
    profile_photo: Optional[str] = None
    field_of_study: Optional[str] = None
    level:         Optional[str] = None
    bio:           Optional[str] = None


class AddSkillRequest(BaseModel):
    """Ajouter une compétence au profil : POST /api/users/me/skills"""
    skill_id:    int
    proficiency: str   # 'strong' ou 'weak'


class SkillResponse(BaseModel):
    """Une compétence telle que retournée par GET /api/skills"""
    id:   int
    name: str

    class Config:
        from_attributes = True


class AddAvailabilityRequest(BaseModel):
    """Ajouter un créneau : POST /api/users/me/availabilities"""
    day_of_week: str
    start_time:  time
    end_time:    time
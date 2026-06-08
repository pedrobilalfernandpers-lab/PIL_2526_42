# schemas/post_schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, time


class PostAvailabilityIn(BaseModel):
    """Créneau envoyé lors de la création d'un post"""
    day_of_week: str
    start_time:  time
    end_time:    time


class PostAvailabilityOut(PostAvailabilityIn):
    """Créneau renvoyé dans une réponse (avec son id BDD)"""
    id: int

    class Config:
        from_attributes = True


class CreatePostRequest(BaseModel):
    """Données pour créer un post : POST /api/posts"""
    type:          str             # 'offer' ou 'request'
    skill_id:      int
    mode:          str             # 'online', 'offline', 'both'
    description:   Optional[str]  = None
    availabilities: List[PostAvailabilityIn] = []


class UpdatePostRequest(BaseModel):
    """Modification partielle : PUT /api/posts/{id}"""
    mode:        Optional[str]  = None
    description: Optional[str]  = None
    is_active:   Optional[bool] = None


class PostResponse(BaseModel):
    """Un post tel que retourné par l'API"""
    id:            int
    user_id:       int
    type:          str
    skill_id:      int
    skill_name:    str   # nom de la compétence (depuis la jointure avec skills)
    mode:          str
    description:   Optional[str]
    is_active:     bool
    availabilities: List[PostAvailabilityOut] = []
    created_at:    datetime

    class Config:
        from_attributes = True
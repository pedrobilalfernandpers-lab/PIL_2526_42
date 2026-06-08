# schemas/message_schema.py

from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SendMessageRequest(BaseModel):
    """Corps de la requête POST /api/conversations/{id}/messages"""
    content: str


class MessageResponse(BaseModel):
    """Un message dans une conversation"""
    id:              int
    conversation_id: int
    sender_id:       int
    sender_name:     str   # prénom + nom (calculé dans le routeur)
    content:         str
    is_read:         bool
    created_at:      datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    """Une conversation dans la liste des conversations"""
    id:               int
    match_id:         int
    other_user_id:    int
    other_user_name:  str
    other_user_photo: Optional[str]
    last_message:     Optional[str]       # contenu du dernier message
    last_message_time: Optional[datetime]
    unread_count:     int                 # nb de messages non lus
    created_at:       datetime

    class Config:
        from_attributes = True
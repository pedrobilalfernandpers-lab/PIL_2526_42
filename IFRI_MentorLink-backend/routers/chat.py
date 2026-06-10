# routers/chat.py

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect, Query, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict
import json

from database import get_db
from models.conversation import Conversation
from models.match import Match
from models.message import Message
from models.user import User
from schemas.message_schema import SendMessageRequest
from services.auth_service import get_current_user, decode_token
from services.chat_service import get_conversation_or_403

router = APIRouter()

# ── WEBSOCKET MANAGER ────────────────────────────────────────

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, websocket: WebSocket, user_id: int):
        await websocket.accept()
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_personal_message(self, message: str, user_id: int):
        if user_id in self.active_connections:
            try:
                await self.active_connections[user_id].send_text(message)
            except Exception as e:
                print(f"Erreur WebSocket pour user {user_id}: {e}")

manager = ConnectionManager()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, token: str = Query(...)):
    user_id = decode_token(token)
    if not user_id:
        await websocket.close(code=1008)
        return
        
    await manager.connect(websocket, user_id)
    try:
        while True:
            # Maintenir la connexion ouverte
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id)

async def notify_user(user_id: int, message_payload: dict):
    await manager.send_personal_message(json.dumps(message_payload), user_id)


@router.get("/conversations")
def get_my_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Liste toutes les conversations de l'utilisateur (matches acceptés)"""

    # Trouve tous les matches acceptés où l'utilisateur est mentor ou mentoré
    matches = db.query(Match).filter(
        Match.status == "accepted",
        (Match.mentor_id == current_user.id) | (Match.mentee_id == current_user.id)
    ).all()

    result = []
    for match in matches:
        conv = db.query(Conversation).filter(
            Conversation.match_id == match.id
        ).first()
        if not conv:
            continue

        # Identifier l'autre utilisateur dans la conversation
        other_id   = match.mentee_id if match.mentor_id == current_user.id else match.mentor_id
        other_user = db.query(User).filter(User.id == other_id).first()
        
        if not other_user:
            continue

        # Dernier message
        last_msg = db.query(Message).filter(
            Message.conversation_id == conv.id
        ).order_by(Message.created_at.desc()).first()

        # Nombre de messages non lus (envoyés par l'autre, pas encore lus)
        unread = db.query(Message).filter(
            Message.conversation_id == conv.id,
            Message.sender_id != current_user.id,
            Message.is_read == False
        ).count()

        result.append({
            "id":               conv.id,
            "match_id":         match.id,
            "subject":          match.skill.name if match.skill else "Général",
            "role":             "Mentor" if match.mentor_id == current_user.id else "Mentoré",
            "other_user_id":    other_user.id,
            "other_user_name":  f"{other_user.first_name} {other_user.last_name}",
            "other_user_photo": other_user.profile_photo,
            "last_message":     last_msg.content if last_msg else None,
            "last_message_time": last_msg.created_at if last_msg else None,
            "unread_count":     unread,
            "created_at":       conv.created_at,
        })

    # Trier par dernier message (conversations les plus actives en premier)
    result.sort(key=lambda c: c["last_message_time"] or c["created_at"], reverse=True)
    return result


@router.get("/conversations/{conv_id}/messages")
def get_messages(
    conv_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne l'historique des messages d'une conversation"""
    conv = get_conversation_or_403(conv_id, current_user, db)

    messages = db.query(Message).filter(
        Message.conversation_id == conv.id
    ).order_by(Message.created_at.asc()).all()

    return [
        {
            "id":              m.id,
            "sender_id":       m.sender_id,
            "sender_name":     f"{m.sender.first_name} {m.sender.last_name}",
            "content":         m.content,
            "is_read":         m.is_read,
            "created_at":      m.created_at,
        }
        for m in messages
    ]


@router.post("/conversations/{conv_id}/messages", status_code=201)
def send_message(
    conv_id: int,
    payload: SendMessageRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Envoie un message dans une conversation"""
    # get_conversation_or_403 vérifie : conv existe + match accepté + user membre
    conv = get_conversation_or_403(conv_id, current_user, db)

    new_message = Message(
        conversation_id = conv.id,
        sender_id       = current_user.id,
        content         = payload.content,
    )
    db.add(new_message)

    # Met à jour updated_at de la conversation
    conv.updated_at = new_message.created_at

    db.commit()
    db.refresh(new_message)

    # Déterminer le destinataire
    other_id = conv.match.mentee_id if conv.match.mentor_id == current_user.id else conv.match.mentor_id

    # Notifier le destinataire en temps réel
    background_tasks.add_task(
        notify_user,
        other_id,
        {
            "type": "new_message",
            "conversation_id": conv.id,
            "message": {
                "id": new_message.id,
                "sender_id": current_user.id,
                "sender_name": f"{current_user.first_name} {current_user.last_name}",
                "content": new_message.content,
                "is_read": False,
                "created_at": new_message.created_at.isoformat()
            }
        }
    )

    return {"message": "Message envoyé.", "id": new_message.id}


@router.put("/messages/{message_id}/read")
def mark_as_read(
    message_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Marque un message comme lu"""
    message = db.query(Message).filter(Message.id == message_id).first()

    if not message or message.sender_id == current_user.id:
        # On ne marque pas ses propres messages comme lus
        return {"message": "Rien à faire."}

    setattr(message, "is_read", True)
    db.commit()
    return {"message": "Message marqué comme lu."}
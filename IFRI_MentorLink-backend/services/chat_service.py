# services/chat_service.py
# Vérifie les droits d'accès à une conversation avant tout envoi de message

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from models.conversation import Conversation
from models.match import Match
from models.user import User


def get_conversation_or_403(
    conversation_id: int,
    current_user: User,
    db: Session
) -> Conversation:
    """
    Récupère une conversation en vérifiant que :
    1. La conversation existe
    2. Le match associé est bien 'accepted'
    3. L'utilisateur courant est bien le mentor ou le mentoré

    Lève une erreur 403 (Forbidden) si une condition échoue.
    C'est LA règle métier principale de la messagerie.
    """
    conversation = db.query(Conversation).filter(
        Conversation.id == conversation_id
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation introuvable."
        )

    match = db.query(Match).filter(Match.id == conversation.match_id).first()

    if match.status != "accepted":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cette conversation n'est pas accessible (match non accepté)."
        )

    if current_user.id not in (match.mentor_id, match.mentee_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'êtes pas membre de cette conversation."
        )

    return conversation
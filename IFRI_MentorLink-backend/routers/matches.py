# routers/matches.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.match import Match
from models.conversation import Conversation
from models.skill import Skill
from models.user import User
from services.auth_service import get_current_user
from services.matching_service import compute_matches_for_user

router = APIRouter()


@router.get("")
def get_my_matches(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Calcule et retourne tous les matches de l'utilisateur connecté.
    Appelle l'algorithme de matching, sauvegarde les nouveaux matches,
    puis retourne la liste triée par score décroissant.
    """
    matches = compute_matches_for_user(db, current_user)

    result = []
    for m in matches:
        skill = db.query(Skill).filter(Skill.id == m.skill_id).first()
        mentor = db.query(User).filter(User.id == m.mentor_id).first()
        mentee = db.query(User).filter(User.id == m.mentee_id).first()

        result.append({
            "id":         m.id,
            "status":     m.status,
            "score":      float(m.score),
            "skill_id":   m.skill_id,
            "skill_name": skill.name if skill else None,
            "mentor": {
                "id": mentor.id,
                "first_name": mentor.first_name,
                "last_name":  mentor.last_name,
                "field_of_study": mentor.field_of_study,
                "level": mentor.level,
                "profile_photo": mentor.profile_photo,
            },
            "mentee": {
                "id": mentee.id,
                "first_name": mentee.first_name,
                "last_name":  mentee.last_name,
                "field_of_study": mentee.field_of_study,
                "level": mentee.level,
                "profile_photo": mentee.profile_photo,
            },
        })

    return result


@router.put("/{match_id}/accept")
def accept_match(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Accepte un match.
    Crée automatiquement une conversation si le match est accepté.
    """
    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=404, detail="Match introuvable.")
    if current_user.id not in (match.mentor_id, match.mentee_id):
        raise HTTPException(status_code=403, detail="Vous n'êtes pas concerné par ce match.")

    match.status = "accepted"

    # Créer la conversation liée à ce match (si elle n'existe pas encore)
    existing_conv = db.query(Conversation).filter(
        Conversation.match_id == match.id
    ).first()

    if not existing_conv:
        db.add(Conversation(match_id=match.id))

    db.commit()
    return {"message": "Match accepté. Conversation ouverte."}


@router.put("/{match_id}/reject")
def reject_match(
    match_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Refuse un match"""
    match = db.query(Match).filter(Match.id == match_id).first()

    if not match:
        raise HTTPException(status_code=404, detail="Match introuvable.")
    if current_user.id not in (match.mentor_id, match.mentee_id):
        raise HTTPException(status_code=403, detail="Action non autorisée.")

    match.status = "rejected"
    db.commit()
    return {"message": "Match refusé."}
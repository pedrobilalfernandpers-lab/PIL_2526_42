# routers/skills.py

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.skill import Skill
from schemas.user_schema import SkillResponse

router = APIRouter()


@router.get("", response_model=List[SkillResponse])
def get_all_skills(db: Session = Depends(get_db)):
    """
    Retourne toutes les compétences disponibles.
    Route publique — pas de JWT nécessaire.
    Utilisée par le formulaire d'inscription pour remplir les listes de compétences.
    """
    return db.query(Skill).order_by(Skill.name).all()
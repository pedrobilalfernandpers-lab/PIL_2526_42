# routers/users.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User, UserSkill, UserAvailability
from schemas.user_schema import (
    UserProfileResponse, UpdateProfileRequest,
    AddSkillRequest, AddAvailabilityRequest
)
from services.auth_service import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retourne le profil complet de l'utilisateur connecté"""
    return current_user


@router.get("/{user_id}", response_model=UserProfileResponse)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retourne le profil complet d'un autre utilisateur"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    return user


@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    payload: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Modifie les infos du profil — seuls les champs fournis sont mis à jour"""
    update_data = payload.model_dump(exclude_none=True)  # ignore les champs None
    for field, value in update_data.items():
        setattr(current_user, field, value)

    db.commit()
    db.refresh(current_user)
    return current_user


# ── COMPÉTENCES ──────────────────────────────────────────────

@router.post("/me/skills", status_code=201)
def add_skill(
    payload: AddSkillRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ajoute une compétence au profil (strong ou weak)"""
    existing = db.query(UserSkill).filter(
        UserSkill.user_id  == current_user.id,
        UserSkill.skill_id == payload.skill_id
    ).first()

    if existing:
        # Met à jour le niveau si la compétence existe déjà
        setattr(existing, "proficiency", payload.proficiency)
        db.commit()
        return {"message": "Compétence mise à jour."}

    new_skill = UserSkill(
        user_id     = current_user.id,
        skill_id    = payload.skill_id,
        proficiency = payload.proficiency
    )
    db.add(new_skill)
    db.commit()
    return {"message": "Compétence ajoutée."}


@router.delete("/me/skills/{skill_id}", status_code=204)
def remove_skill(
    skill_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime une compétence du profil"""
    skill = db.query(UserSkill).filter(
        UserSkill.user_id  == current_user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if not skill:
        raise HTTPException(status_code=404, detail="Compétence introuvable.")

    db.delete(skill)
    db.commit()


# ── DISPONIBILITÉS ────────────────────────────────────────────

@router.post("/me/availabilities", status_code=201)
def add_availability(
    payload: AddAvailabilityRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Ajoute un créneau de disponibilité"""
    new_avail = UserAvailability(
        user_id     = current_user.id,
        day_of_week = payload.day_of_week,
        start_time  = payload.start_time,
        end_time    = payload.end_time
    )
    db.add(new_avail)
    db.commit()
    db.refresh(new_avail)
    return {"message": "Disponibilité ajoutée.", "id": new_avail.id}


@router.delete("/me/availabilities/{avail_id}", status_code=204)
def remove_availability(
    avail_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Supprime un créneau de disponibilité"""
    avail = db.query(UserAvailability).filter(
        UserAvailability.id      == avail_id,
        UserAvailability.user_id == current_user.id
    ).first()

    if not avail:
        raise HTTPException(status_code=404, detail="Disponibilité introuvable.")

    db.delete(avail)
    db.commit()
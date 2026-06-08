# routers/auth.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from schemas.auth_schema import RegisterRequest, LoginRequest, TokenResponse, PasswordResetRequest
from services.auth_service import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=201)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    """Inscription d'un nouvel utilisateur"""

    # Vérifier unicité email
    if db.query(User).filter(User.email == payload.email).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Cet email est déjà utilisé."
        )

    # Vérifier unicité téléphone
    if db.query(User).filter(User.phone_number == payload.phone_number).first():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ce numéro de téléphone est déjà utilisé."
        )

    # Créer l'utilisateur avec le mot de passe haché
    new_user = User(
        first_name    = payload.first_name,
        last_name     = payload.last_name,
        email         = payload.email,
        phone_number  = payload.phone_number,
        password_hash = hash_password(payload.password),  # jamais en clair
        field_of_study = payload.field_of_study,
        level         = payload.level,
        bio           = payload.bio,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Retourner un token directement → l'utilisateur est connecté après inscription
    token = create_access_token(new_user.id)
    return TokenResponse(
        access_token = token,
        user_id      = new_user.id,
        first_name   = new_user.first_name,
        last_name    = new_user.last_name,
    )


@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """Connexion avec email OU téléphone + mot de passe"""

    # Chercher l'utilisateur par email ou téléphone
    user = db.query(User).filter(
        (User.email == payload.identifier) |
        (User.phone_number == payload.identifier)
    ).first()

    # Message volontairement générique pour ne pas révéler si l'email existe
    if not user or not verify_password(payload.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Identifiant ou mot de passe incorrect."
        )

    token = create_access_token(user.id)
    return TokenResponse(
        access_token = token,
        user_id      = user.id,
        first_name   = user.first_name,
        last_name    = user.last_name,
    )


@router.post("/reset-password")
def reset_password(payload: PasswordResetRequest, db: Session = Depends(get_db)):
    """Réinitialisation du mot de passe"""

    user = db.query(User).filter(
        (User.email == payload.identifier) |
        (User.phone_number == payload.identifier)
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aucun compte associé à cet identifiant."
        )

    user.password_hash = hash_password(payload.new_password)
    db.commit()
    return {"message": "Mot de passe mis à jour avec succès."}
# schemas/auth_schema.py
# Données attendues pour l'inscription et la connexion

from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequest(BaseModel):
    """Données envoyées par le formulaire d'inscription"""
    first_name:    str
    last_name:     str
    email:         EmailStr   # Pydantic vérifie automatiquement le format email
    phone_number:  str
    password:      str        # mot de passe en clair → haché dans auth_service.py
    field_of_study: str
    level:         str
    bio:           Optional[str] = None


class LoginRequest(BaseModel):
    """Connexion : email OU téléphone + mot de passe"""
    identifier: str   # peut être email ou numéro de téléphone
    password:   str


class TokenResponse(BaseModel):
    """Ce que le serveur renvoie après une connexion réussie"""
    access_token: str
    token_type:   str = "bearer"
    user_id:      int
    first_name:   str
    last_name:    str


class PasswordResetRequest(BaseModel):
    """Réinitialisation du mot de passe"""
    identifier:   str   # email ou téléphone
    new_password: str
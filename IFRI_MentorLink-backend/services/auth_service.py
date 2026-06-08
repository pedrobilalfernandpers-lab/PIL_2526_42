# services/auth_service.py

from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from database import get_db
from models.user import User

# Contexte bcrypt pour le hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Indique à FastAPI où chercher le token dans les requêtes
# Il cherchera un header : Authorization: Bearer <token>
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


# ── MOTS DE PASSE ────────────────────────────────────────────

def hash_password(password: str) -> str:
    """Transforme un mot de passe en clair en hash bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie qu'un mot de passe correspond à son hash"""
    return pwd_context.verify(plain_password, hashed_password)


# ── TOKENS JWT ───────────────────────────────────────────────

def create_access_token(user_id: int) -> str:
    """
    Crée un token JWT signé contenant l'id de l'utilisateur.
    Le token expire après ACCESS_TOKEN_EXPIRE_MINUTES minutes.
    """
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": str(user_id),   # "sub" = subject = identifiant principal
        "exp": expire          # date d'expiration
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> Optional[int]:
    """
    Décode un token JWT et retourne l'user_id.
    Retourne None si le token est invalide ou expiré.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        return int(user_id)
    except JWTError:
        return None


# ── DÉPENDANCE FASTAPI ───────────────────────────────────────

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance injectée dans tous les routeurs protégés.
    Usage : current_user: User = Depends(get_current_user)

    Elle lit le token JWT dans le header Authorization,
    le vérifie, et retourne l'utilisateur connecté.
    Lance une erreur 401 si le token est absent ou invalide.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré. Veuillez vous reconnecter.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user_id = decode_token(token)
    if user_id is None:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    return user
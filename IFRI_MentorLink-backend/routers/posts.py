# routers/posts.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db
from models.mentorship_post import MentorshipPost, PostAvailability
from models.skill import Skill
from models.user import User
from schemas.post_schema import CreatePostRequest, UpdatePostRequest, PostResponse
from services.auth_service import get_current_user

router = APIRouter()


@router.get("", response_model=List[PostResponse])
def get_posts(
    type: Optional[str]    = None,   # filtrer par 'offer' ou 'request'
    skill_id: Optional[int] = None,  # filtrer par compétence
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Liste tous les posts actifs avec filtres optionnels"""
    query = db.query(MentorshipPost).filter(MentorshipPost.is_active == True)

    if type:
        query = query.filter(MentorshipPost.type == type)
    if skill_id:
        query = query.filter(MentorshipPost.skill_id == skill_id)

    posts = query.order_by(MentorshipPost.created_at.desc()).all()

    # Enrichir chaque post avec le nom de la compétence et les infos de l'auteur
    result = []
    for post in posts:
        skill = db.query(Skill).filter(Skill.id == post.skill_id).first()
        setattr(post, "skill_name", skill.name if skill else "")
        setattr(post, "user_name", f"{post.user.first_name} {post.user.last_name}")
        setattr(post, "user_photo", post.user.profile_photo)
        result.append(PostResponse.model_validate(post))
    return result


@router.post("", status_code=201)
def create_post(
    payload: CreatePostRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Crée un nouveau post (offre ou demande)"""
    new_post = MentorshipPost(
        user_id     = current_user.id,
        type        = payload.type,
        skill_id    = payload.skill_id,
        mode        = payload.mode,
        description = payload.description,
    )
    db.add(new_post)
    db.flush()  # génère l'id sans commit pour pouvoir l'utiliser tout de suite

    # Ajouter les créneaux de disponibilité liés à ce post
    for avail in payload.availabilities:
        db.add(PostAvailability(
            post_id     = new_post.id,
            day_of_week = avail.day_of_week,
            start_time  = avail.start_time,
            end_time    = avail.end_time,
        ))

    db.commit()
    db.refresh(new_post)
    return {"message": "Post créé avec succès.", "id": new_post.id}


@router.put("/{post_id}")
def update_post(
    post_id: int,
    payload: UpdatePostRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Modifie un post — seulement si c'est le sien"""
    post = db.query(MentorshipPost).filter(MentorshipPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post introuvable.")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Vous ne pouvez modifier que vos propres posts.")

    for field, value in payload.model_dump(exclude_none=True).items():
        setattr(post, field, value)

    db.commit()
    return {"message": "Post mis à jour."}


@router.delete("/{post_id}", status_code=204)
def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Archive un post (is_active = False) plutôt que de le supprimer"""
    post = db.query(MentorshipPost).filter(MentorshipPost.id == post_id).first()

    if not post:
        raise HTTPException(status_code=404, detail="Post introuvable.")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Action non autorisée.")

    setattr(post, "is_active", False)
    db.commit()

@router.post("/{post_id}/apply", status_code=201)
def apply_to_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Postule à une annonce sur le mur.
    Crée un Match (accepté) et une Conversation directe.
    """
    from models.match import Match
    from models.conversation import Conversation
    
    post = db.query(MentorshipPost).filter(MentorshipPost.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Annonce introuvable.")
    
    if post.user_id == current_user.id:
        raise HTTPException(status_code=400, detail="Vous ne pouvez pas postuler à votre propre annonce.")

    # Déterminer qui est le mentor et qui est le mentoré selon le type d'annonce
    if post.type == "offer":
        # L'auteur propose son aide = il est mentor, le postulant est mentoré
        mentor_id = post.user_id
        mentee_id = current_user.id
    else:
        # L'auteur demande de l'aide = il est mentoré, le postulant est mentor
        mentor_id = current_user.id
        mentee_id = post.user_id

    # Vérifier si la conversation existe déjà
    existing_match = db.query(Match).filter(
        Match.mentor_id == mentor_id,
        Match.mentee_id == mentee_id,
        Match.skill_id == post.skill_id
    ).first()

    if existing_match:
        if existing_match.status == "rejected":
            # L'utilisateur avait rompu le match, on le réactive
            setattr(existing_match, "status", "accepted")
            conv = db.query(Conversation).filter(Conversation.match_id == existing_match.id).first()
            if not conv:
                conv = Conversation(match_id=existing_match.id)
                db.add(conv)
            db.commit()
            return {"message": "Match réactivé ! La conversation est de nouveau ouverte.", "conversation_id": conv.id}

        conv = db.query(Conversation).filter(Conversation.match_id == existing_match.id).first()
        if not conv:
            setattr(existing_match, "status", "accepted")
            new_conv = Conversation(match_id=existing_match.id)
            db.add(new_conv)
            db.commit()
            return {"message": "Vous aviez déjà un match. Conversation ouverte !", "conversation_id": new_conv.id}
        return {"message": "Vous êtes déjà en contact avec cet utilisateur.", "conversation_id": conv.id}

    # Créer le nouveau Match manuel
    new_match = Match(
        mentor_id=mentor_id,
        mentee_id=mentee_id,
        skill_id=post.skill_id,
        score=100.0,
        status="accepted",
        offer_post_id=post.id if post.type == "offer" else None,
        request_post_id=post.id if post.type == "request" else None
    )
    db.add(new_match)
    db.flush() 

    # Créer la conversation
    new_conv = Conversation(match_id=new_match.id)
    db.add(new_conv)
    db.commit()
    
    return {"message": "Candidature envoyée ! La conversation est ouverte.", "conversation_id": new_conv.id}
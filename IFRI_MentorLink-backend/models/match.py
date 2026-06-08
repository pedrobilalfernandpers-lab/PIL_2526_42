# models/match.py

from sqlalchemy import (
    Column, Integer, String, ForeignKey,
    TIMESTAMP, Numeric, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Match(Base):
    __tablename__ = "matches"

    id               = Column(Integer, primary_key=True, index=True)
    mentor_id        = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    mentee_id        = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    offer_post_id    = Column(Integer, ForeignKey("mentorship_posts.id"), nullable=True)
    request_post_id  = Column(Integer, ForeignKey("mentorship_posts.id"), nullable=True)
    skill_id         = Column(Integer, ForeignKey("skills.id"), nullable=True)
    score            = Column(Numeric(5, 2), nullable=False, default=0)
    # Score sur 100 : 40 pts compétences + 30 pts horaires + 30 pts filière
    status           = Column(String(20), nullable=False, default="pending")
    # 'pending'  = proposé par l'algo, en attente de réponse
    # 'accepted' = les deux utilisateurs ont accepté → conversation créée
    # 'rejected' = refusé
    created_at       = Column(TIMESTAMP, server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'accepted', 'rejected')",
            name="chk_match_status"
        ),
        CheckConstraint("mentor_id != mentee_id", name="chk_mentor_mentee_diff"),
    )

    # foreign_keys explicite car 2 FKs vers la même table (users)
    mentor  = relationship("User", foreign_keys=[mentor_id],
                           back_populates="mentor_matches")
    mentee  = relationship("User", foreign_keys=[mentee_id],
                           back_populates="mentee_matches")
    skill   = relationship("Skill", back_populates="matches")

    # uselist=False = relation 1:1 (un match = une seule conversation)
    conversation = relationship("Conversation", back_populates="match",
                                uselist=False)
# models/mentorship_post.py

from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    ForeignKey, TIMESTAMP, Time, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ──────────────────────────────────────────
# TABLE: mentorship_posts
# Une offre OU une demande de mentorat
# ──────────────────────────────────────────
class MentorshipPost(Base):
    __tablename__ = "mentorship_posts"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False, index=True)
    type        = Column(String(10), nullable=False)
    # 'offer'   = "je peux aider en Python"
    # 'request' = "j'ai besoin d'aide en SQL"
    skill_id    = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    mode        = Column(String(10), nullable=False)
    # 'online', 'offline', 'both'
    description = Column(Text,    nullable=True)
    is_active   = Column(Boolean, default=True)
    # False = post archivé (invisible dans les recherches)
    created_at  = Column(TIMESTAMP, server_default=func.now())
    updated_at  = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("type IN ('offer', 'request')",         name="chk_post_type"),
        CheckConstraint("mode IN ('online', 'offline', 'both')", name="chk_post_mode"),
    )

    user          = relationship("User",             back_populates="posts")
    skill         = relationship("Skill",            back_populates="posts")
    availabilities = relationship("PostAvailability", back_populates="post",
                                  cascade="all, delete-orphan")


# ──────────────────────────────────────────
# TABLE: post_availabilities
# Les créneaux horaires spécifiques à un post
# ──────────────────────────────────────────
class PostAvailability(Base):
    __tablename__ = "post_availabilities"

    id          = Column(Integer, primary_key=True, index=True)
    post_id     = Column(Integer, ForeignKey("mentorship_posts.id", ondelete="CASCADE"),
                         nullable=False)
    day_of_week = Column(String(10), nullable=False)
    start_time  = Column(Time, nullable=False)
    end_time    = Column(Time, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "day_of_week IN ('Monday','Tuesday','Wednesday','Thursday',"
            "'Friday','Saturday','Sunday')",
            name="chk_post_avail_day"
        ),
        CheckConstraint("start_time < end_time", name="chk_post_avail_time"),
    )

    post = relationship("MentorshipPost", back_populates="availabilities")
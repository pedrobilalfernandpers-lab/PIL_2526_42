# models/user.py

from sqlalchemy import (
    Column, Integer, String, Text, Boolean,
    ForeignKey, TIMESTAMP, Time, CheckConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ──────────────────────────────────────────
# TABLE: users
# ──────────────────────────────────────────
class User(Base):
    __tablename__ = "users"

    id            = Column(Integer, primary_key=True, index=True)
    first_name    = Column(String(50),  nullable=False)
    last_name     = Column(String(50),  nullable=False)
    email         = Column(String(100), nullable=False, unique=True, index=True)
    phone_number  = Column(String(20),  nullable=False, unique=True)
    password_hash = Column(String(255), nullable=False)
    profile_photo = Column(String(255), nullable=True)   # URL, peut être NULL
    field_of_study = Column(String(50), nullable=False)  # IA, IM, GL, SE&IoT, SI
    level         = Column(String(20),  nullable=False)  # L1, L2, L3, M1, M2
    bio           = Column(Text,        nullable=True)
    created_at    = Column(TIMESTAMP,   server_default=func.now())
    updated_at    = Column(TIMESTAMP,   server_default=func.now(), onupdate=func.now())

    # Relations :
    # "cascade=all, delete-orphan" = si on supprime un user,
    # ses skills/dispo/posts sont supprimés automatiquement
    skills          = relationship("UserSkill",      back_populates="user",
                                   cascade="all, delete-orphan")
    availabilities  = relationship("UserAvailability", back_populates="user",
                                   cascade="all, delete-orphan")
    posts           = relationship("MentorshipPost", back_populates="user",
                                   cascade="all, delete-orphan")

    # Un user peut être mentor dans plusieurs matches
    # ET mentoré dans d'autres → 2 relations séparées avec foreign_keys explicite
    mentor_matches  = relationship("Match", foreign_keys="Match.mentor_id",
                                   back_populates="mentor")
    mentee_matches  = relationship("Match", foreign_keys="Match.mentee_id",
                                   back_populates="mentee")

    sent_messages   = relationship("Message", back_populates="sender")


# ──────────────────────────────────────────
# TABLE: user_skills
# Relation many-to-many entre users et skills
# avec un attribut supplémentaire : proficiency
# ──────────────────────────────────────────
class UserSkill(Base):
    __tablename__ = "user_skills"

    # Clé primaire composée : (user_id, skill_id) = unique ensemble
    user_id     = Column(Integer, ForeignKey("users.id",  ondelete="CASCADE"),
                         primary_key=True)
    skill_id    = Column(Integer, ForeignKey("skills.id", ondelete="CASCADE"),
                         primary_key=True)
    proficiency = Column(String(10), nullable=False)
    # 'strong' = maîtrisé (peut enseigner)
    # 'weak'   = lacune (besoin d'aide)

    __table_args__ = (
        CheckConstraint("proficiency IN ('strong', 'weak')", name="chk_proficiency"),
    )

    user  = relationship("User",  back_populates="skills")
    skill = relationship("Skill", back_populates="user_skills")

    @property
    def skill_name(self):
        return self.skill.name if self.skill else None


# ──────────────────────────────────────────
# TABLE: user_availabilities
# Les créneaux horaires habituels du profil utilisateur
# ──────────────────────────────────────────
class UserAvailability(Base):
    __tablename__ = "user_availabilities"

    id          = Column(Integer, primary_key=True, index=True)
    user_id     = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"),
                         nullable=False)
    day_of_week = Column(String(10), nullable=False)
    # ex: 'Monday', 'Tuesday', 'Wednesday'...
    start_time  = Column(Time, nullable=False)  # ex: 14:00
    end_time    = Column(Time, nullable=False)  # ex: 17:00

    __table_args__ = (
        CheckConstraint(
            "day_of_week IN ('Monday','Tuesday','Wednesday','Thursday',"
            "'Friday','Saturday','Sunday')",
            name="chk_user_avail_day"
        ),
        CheckConstraint("start_time < end_time", name="chk_user_avail_time"),
    )

    user = relationship("User", back_populates="availabilities")
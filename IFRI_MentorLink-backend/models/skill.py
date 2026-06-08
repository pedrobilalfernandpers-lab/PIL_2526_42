# models/skill.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base


class Skill(Base):
    __tablename__ = "skills"

    id   = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, unique=True)
    # ex: "Algorithmique", "Python", "SQL", "Réseaux"...

    # Relations (utiles pour les jointures dans le matching)
    user_skills = relationship("UserSkill",      back_populates="skill")
    posts       = relationship("MentorshipPost", back_populates="skill")
    matches     = relationship("Match",          back_populates="skill")
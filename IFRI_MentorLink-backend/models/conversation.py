# models/conversation.py

from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id         = Column(Integer, primary_key=True, index=True)
    match_id   = Column(Integer, ForeignKey("matches.id", ondelete="CASCADE"),
                        nullable=False, unique=True)
    # unique=True = un seul match → une seule conversation (relation 1:1)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    # updated_at se met à jour automatiquement à chaque nouveau message

    match    = relationship("Match", back_populates="conversation")
    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
        order_by="Message.created_at"  # messages toujours dans l'ordre chronologique
    )
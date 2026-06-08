# models/message.py

from sqlalchemy import Column, Integer, Boolean, Text, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


class Message(Base):
    __tablename__ = "messages"

    id              = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey("conversations.id", ondelete="CASCADE"),
                             nullable=False, index=True)
    sender_id       = Column(Integer, ForeignKey("users.id"), nullable=False)
    content         = Column(Text,    nullable=False)
    is_read         = Column(Boolean, default=False)
    # False = message non lu par le destinataire
    # True  = message lu (mis à jour par PUT /api/messages/{id}/read)
    created_at      = Column(TIMESTAMP, server_default=func.now())

    conversation = relationship("Conversation", back_populates="messages")
    sender       = relationship("User",         back_populates="sent_messages")
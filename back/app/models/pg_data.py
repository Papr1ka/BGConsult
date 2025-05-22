from sqlalchemy import (
    Column, BigInteger, Integer, String, Text,
    Boolean, TIMESTAMP, ForeignKey, SmallInteger
)
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.sql import func

from back.app.core.storage.postgres import Base


class Dialog(Base):
    __tablename__ = "dialogs"

    dialog_id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, nullable=False)
    user_name = Column(String(100), nullable=False)
    started_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    ended_at = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(String(20), nullable=True)

    # Relationships
    messages = relationship("Message", back_populates="dialog", cascade="all, delete-orphan")
    ratings = relationship("Rating", back_populates="dialog", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"

    message_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dialog_id = Column(BigInteger, ForeignKey("dialogs.dialog_id"), nullable=False)
    text = Column(Text, nullable=True)
    is_from_user = Column(Boolean, nullable=False)
    sent_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship
    dialog = relationship("Dialog", back_populates="messages")


class Rating(Base):
    __tablename__ = "ratings"

    rating_id = Column(BigInteger, primary_key=True, autoincrement=True)
    dialog_id = Column(BigInteger, ForeignKey("dialogs.dialog_id"), nullable=False)
    score = Column(SmallInteger, nullable=False)
    rated_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    # Relationship
    dialog = relationship("Dialog", back_populates="ratings")

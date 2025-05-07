import os
import uuid
from datetime import datetime
from sqlalchemy import (
    create_engine, Column, String, Text, DateTime, Integer
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


DB_URL =  "sqlite:///chat_memory.db"
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)        # 'user' ou 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(bind=engine)

class ChatMemory:
    @staticmethod
    def create_session() -> str:
        """Génère un nouveau session_id."""
        return str(uuid.uuid4())

    @staticmethod
    def get_history(session_id: str, limit: int = 10):
        db = SessionLocal()
        msgs = (
            db.query(ChatMessage)
              .filter(ChatMessage.session_id == session_id)
              .order_by(ChatMessage.timestamp.asc())
              .all()
        )
        db.close()
        return [{"role": m.role, "content": m.content} for m in msgs[-limit:]]

    @staticmethod
    def add_message(session_id: str, role: str, content: str):
        db = SessionLocal()
        msg = ChatMessage(session_id=session_id, role=role, content=content)
        db.add(msg)
        db.commit()
        db.close()

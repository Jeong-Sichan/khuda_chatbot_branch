from sqlalchemy import Column, Integer, Text, text
from database import Base

class Message(Base):
    __tablename__ = "messages"   # 실제 DB 안 테이블 이름

    id = Column(Integer, primary_key=True, autoincrement=True)  # 자동 번호표
    session_id = Column(Text, nullable=True)    # 어느 대화방인지
    parent_id = Column(Integer, nullable=True)  # 부모의 id
    role = Column(Text, nullable=False)         # "user" 또는 "assistant"
    content = Column(Text, nullable=False)      # 실제 메시지 내용
    created_at = Column(
        Text, nullable=False,
        server_default=text("(datetime('now'))"),  # 저장된 시각 자동 기록
    )

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Text, primary_key=True)        # UUID 문자열
    title = Column(Text, nullable=False, server_default="새 대화")
    created_at = Column(
        Text, nullable=False,
        server_default=text("(datetime('now'))"),
    )

class Branch(Base):
    __tablename__ = "branches"
    id = Column(Text, primary_key=True)            # UUID
    session_id = Column(Text, nullable=False)      # 어느 대화방 소속
    name = Column(Text, nullable=False, server_default="main")
    head_id = Column(Integer, nullable=True)       # 이 가지의 현재 잎 (= git HEAD)
    created_at = Column(Text, nullable=False, server_default=text("(datetime('now'))"))
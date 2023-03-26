from datetime import datetime
import uuid
from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import (JSON, TIMESTAMP, Boolean, Column, DateTime, ForeignKey, Integer,
                        String, Table, UUID)
from sqlalchemy.orm import relationship, backref
from utils.base import Base

role = Table(
    "role",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)
photos = Table(
    "photos",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)
posts = Table(
    "posts",
    Base.metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("permissions", JSON),
)

user_chat = Table(
    'user_chat',
    Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('chat_id', Integer, ForeignKey('chats.id'))
)


class Chat(Base):
    __tablename__ = 'chats'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship('Message', backref='chat')

# Define the association table between User and Chat


class User(SQLAlchemyBaseUserTableUUID, Base):
    __tablename__ = "user"
    __table_args__ = {'extend_existing': True}

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, nullable=False)
    avatar = Column(String, nullable=True)
    username = Column(String, nullable=False)
    role_id = Column(Integer, ForeignKey(role.c.id))
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    hashed_password: str = Column(String(length=1024), nullable=False)

    chats = relationship('Chat', secondary='user_chat', backref='users')
    posts = relationship("Post", backref="user", lazy="dynamic")
    photos = relationship("Photo", backref="user", lazy="dynamic")
    is_active: bool = Column(Boolean, default=True, nullable=False)
    is_superuser: bool = Column(Boolean, default=False, nullable=False)
    is_verified: bool = Column(Boolean, default=False, nullable=False)


class Message(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True)
    text = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    chat_id = Column(Integer, ForeignKey('chats.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship('User', backref=backref('messages', order_by=id))

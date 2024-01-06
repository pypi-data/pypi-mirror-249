from __future__ import annotations

import random

import sqlalchemy as sa
import sqlalchemy.orm as sa_orm

from sqlalchemy_sessionload.loaders import (
    iter_session_mapper_instances,
    load_by_primary_key,
    load_from_session,
)

from .model import Message, User

message_mapper = Message.__mapper__


def test_iter_session_mapper_instances(db_session: sa_orm.Session):
    messages = db_session.query(Message).all()

    iter_values = list(iter_session_mapper_instances(db_session, message_mapper))

    for message in messages:
        assert message in iter_values


def test_load_by_primary_key(db_session: sa_orm.Session):
    message: Message | None = db_session.query(Message).first()
    assert message is not None
    loaded_message = load_by_primary_key(
        db_session,
        message_mapper,
        sa.select(Message).where(Message.message_id == message.message_id),
    )
    assert loaded_message is message


def test_basic_load_from_session(db_session: sa_orm.Session):
    messages = db_session.query(Message).all()
    loaded_messages = load_from_session(db_session, message_mapper, sa.select(Message))
    for message in messages:
        assert message in loaded_messages


def test_filtered_load_from_session(db_session):
    user = db_session.get(User, (5,))
    query = sa.select(Message).filter(
        sa.and_(
            Message.user_id == user.user_id,
            Message.chatroom_id == random.choice(user.chat_rooms).chatroom_id,
        )
    )
    messages = db_session.execute(query).all()
    loaded_messages = tuple(load_from_session(db_session, message_mapper, query))
    assert len(loaded_messages) == len(messages)
    for row in messages:
        assert row[0] in loaded_messages

import pytest
import sqlalchemy as sa
import sqlalchemy.orm as sa_orm
from pytest_benchmark.fixture import BenchmarkFixture

from sqlalchemy_sessionload.options import SessionLoad, SessionRelationshipLoad

from .model import Chatroom, Message, User


@pytest.mark.benchmark(group="basic-query")
def test_basic_load(db_session: sa_orm.Session, benchmark: BenchmarkFixture):
    messages = db_session.execute(sa.select(Message)).all()

    @benchmark
    def messages():
        stmt = sa.select(Message)
        return db_session.execute(stmt).all()

    assert len(messages) > 0


@pytest.mark.benchmark(group="basic-query")
def test_basic_load_with_option(
    db_session: sa_orm.Session, benchmark: BenchmarkFixture
):
    messages = db_session.execute(sa.select(Message)).all()

    @benchmark
    def loaded_messages():
        stmt = sa.select(Message).options(SessionLoad(Message))
        return db_session.execute(stmt).all()

    for message in messages:
        assert message in loaded_messages


def test_basic_load_with_option_query(db_session: sa_orm.Session):
    messages = db_session.query(Message).all()

    loaded_messages = db_session.query(Message).options(SessionLoad(Message)).all()
    assert len(loaded_messages) == len(messages)
    for message in messages:
        assert message in loaded_messages


def test_equal_result_metadata_keys(db_session: sa_orm.Session):
    messages = db_session.execute(sa.select(Message))

    loaded_messages = db_session.execute(
        sa.select(Message).options(SessionLoad(Message))
    )

    assert loaded_messages._metadata._keys == messages._metadata._keys  # type: ignore


load_option_params = [
    (
        [
            sa_orm.subqueryload(Message.chatroom),
            sa_orm.subqueryload(Message.chatroom, Chatroom.members),
            sa_orm.subqueryload(Message.user),
            sa_orm.subqueryload(Message.user, User.chat_rooms),
        ],
        [
            SessionRelationshipLoad(Message.chatroom, Chatroom.members),
            SessionRelationshipLoad(Message.user, User.chat_rooms),
        ],
    ),
    (
        [
            sa_orm.selectinload(Message.chatroom),
            sa_orm.selectinload(Message.chatroom, Chatroom.members),
            sa_orm.selectinload(Message.user),
            sa_orm.selectinload(Message.user, User.chat_rooms),
        ],
        [
            SessionRelationshipLoad(Message.chatroom, Chatroom.members),
            SessionRelationshipLoad(Message.user, User.chat_rooms),
        ],
    ),
]


@pytest.mark.parametrize(["basic_options", "lib_options"], load_option_params)
@pytest.mark.benchmark(group="relationship-load")
def test_relationship_load(
    db_session: sa_orm.Session, benchmark: BenchmarkFixture, basic_options, lib_options
):
    messages = db_session.execute(sa.select(Message).options(*basic_options)).all()

    @benchmark
    def messages():
        stmt = sa.select(Message).options(*basic_options)
        return db_session.execute(stmt).all()

    assert len(messages) > 0


@pytest.mark.parametrize(["basic_options", "lib_options"], load_option_params)
@pytest.mark.benchmark(group="relationship-load")
def test_relationship_load_option(
    db_session: sa_orm.Session, benchmark: BenchmarkFixture, basic_options, lib_options
):
    messages = [
        row[0]
        for row in db_session.execute(
            sa.select(Message).options(*basic_options),
        )
    ]

    @benchmark
    def loaded_messages():
        stmt = sa.select(Message).options(*basic_options, *lib_options)
        return [row[0] for row in db_session.execute(stmt)]

    messages = sorted(messages, key=lambda message: message.message_id)
    loaded_messages = sorted(loaded_messages, key=lambda message: message.message_id)
    assert len(loaded_messages) == len(messages)
    for message in messages:
        assert message in loaded_messages

    for message, loaded_message in zip(messages, loaded_messages):
        assert loaded_message == message

        assert loaded_message.chatroom == message.chatroom
        assert len(loaded_message.chatroom.members) == len(message.chatroom.members)
        for user in message.chatroom.members:
            assert user in loaded_message.chatroom.members

        assert loaded_message.user == message.user
        assert len(loaded_message.user.chat_rooms) == len(message.user.chat_rooms)
        for chatroom in message.user.chat_rooms:
            assert chatroom in loaded_message.user.chat_rooms

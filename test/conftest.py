import os
import pytest
from sqlalchemy import create_engine
from outlet import db


@pytest.fixture(scope="session")
def sqlalchemy_connect_url():
    yield os.environ['DB_URL']


@pytest.fixture(scope='session')
def connection(request, sqlalchemy_connect_url):
    engine = create_engine(sqlalchemy_connect_url)
    db.Base.metadata.create_all(engine)
    connection = engine.connect()
    db.Session.registry.clear()
    db.Session.configure(bind=connection)
    db.Base.metadata.bind = engine

    def fin():
        db.Base.metadata.drop_all
        connection.close()
    request.addfinalizer(fin)
    return connection


@pytest.fixture
def dbsession(request, connection):
    trans = connection.begin()

    def fin():
        db.Session.close()
        trans.rollback()
        connection.close()
    request.addfinalizer(fin)
    return db.Session()

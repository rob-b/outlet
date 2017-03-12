import pytest
from outlet import server
from webtest import TestApp as FakeApp
from outlet import db


@pytest.fixture
def account(dbsession):
    account = db.new_account(dbsession)
    dbsession.commit()
    yield account


def test_middleware_rejects_non_json():
    app = FakeApp(server.make_app())
    resp = app.post('/', expect_errors=True)
    assert resp.status_code == 415


def test_responds_400_with_empty_body():
    app = FakeApp(server.make_app())
    resp = app.post('/', expect_errors=True, content_type='application/json')
    assert resp.status_code == 400


def test_middleware_accepts_json(dbsession, account):
    app = FakeApp(server.make_app())
    params = {'account_id': account.id, 'amount': 400,
              'user_id': 1001, 'nonce': 'fake-valid-nonce'}
    resp = app.post_json('/', params, expect_errors=True)
    assert resp.status_code == 201

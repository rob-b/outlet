import falcon
import money
import braintree
from braintree.test.nonces import Nonces
from voluptuous import Schema, Required, All
from outlet import db
from sumtypes import sumtype, constructor, match


users = {1001, 2001, 3001}


class GBP(money.Money):
    def __init__(self, amount='0'):
        super().__init__(amount=amount, currency='GBP')


def user():
    def f(u):
        if not (isinstance(u, int) and u in users):
            raise ValueError("User id either invalid or does not exist")
    return f


def account():
    def f(a):
        session = db.Session()
        inner = session.query(db.Account).filter(db.Account.id == a)
        if not session.query(inner.exists()).scalar():
            raise ValueError("Account with id {} does not exist".format(a))
    return f


def valid_money():
    def f(v):
        GBP(v)
    return f


transaction_schema = Schema({
    Required('user_id'): All(user()),
    Required('account_id'): All(account()),
    Required('amount'): valid_money(),
})


def after_create_transaction(req, resp, resource):
    result = req.context.get('result_type')
    if not result:
        return
    result = get_result(result)
    resp.status = falcon.HTTP_201
    req.context['result'] = {'data': result}


@sumtype
class Result:
    Failure = constructor('msg')
    Success = constructor('value')


@match(Result)
class get_result:
    def Failure(msg): raise falcon.HTTPBadRequest(msg)

    def Success(value): return value


def create_user_transaction(session, user_id, amount, account_id):
    # - maximum £500 worth of loads per day
    # - maximum £800 worth of loads per 30 days
    # - maximum £2000 worth of loads per 365 days
    # - maximum balance at any time £1000
    ut = db.UserTransactions(session, user_id)
    if ut.for_days(0) >= 500:
        retval = Result.Failure("Exceeded day's usage")
    elif ut.for_days(30) >= 800:
        retval = Result.Failure("Exceeded months's usage")
    elif ut.for_days(365) >= 2000:
        retval = Result.Failure("Exceeded annual usage")
    elif not(1000 >= ut.total() > -1):
        retval = Result.Failure("Exceeded maximum balance")
    else:

        # NOTE: this is very slow, should really kick off to a job
        result = braintree.Transaction.sale({
            "amount": amount.amount,
            "payment_method_nonce": Nonces.Transactable,
            "options": {
              "submit_for_settlement": True
            }
        })
        if not result.is_success:
            1/0
        session.add(db.new_transaction(user_id, amount.amount, account_id))
        retval = Result.Success("Added {}".format(amount.amount))

    return retval

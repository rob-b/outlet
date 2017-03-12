import falcon
import money
import braintree
from voluptuous import Schema, Required, All
from outlet import db
from sumtypes import sumtype, constructor, match


users = {1001, 2001, 3001}


class GBP(money.Money):
    def __init__(self, amount='0'):
        super().__init__(amount=amount, currency='GBP')


def valid_user():
    def f(u):
        if not (isinstance(u, int) and u in users):
            raise ValueError("User id either invalid or does not exist")
    return f


def valid_account():
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
    Required('user_id'): All(valid_user()),
    Required('account_id'): All(valid_account()),
    Required('amount'): valid_money(),
    Required('nonce'): str,
})


def after_create_transaction(req, resp, resource):
    result = req.context.get('result_type')
    if not result:
        return
    result = match_result(result)
    resp.status = falcon.HTTP_201
    req.context['result'] = {'data': result}


@sumtype
class Result:
    Failure = constructor('msg')
    Success = constructor('value')


@match(Result)
class match_result:
    def Failure(msg): raise falcon.HTTPBadRequest(msg)

    def Success(value): return value


def create_account_transaction(params):
    at = db.AccountTransactions(params.session, params.account_id)
    amount = params.amount
    if at.exceeds_daily_limit(amount):
        retval = Result.Failure("Transaction would exceed day's usage")
    elif at.exceeds_monthly_limit(amount):
        retval = Result.Failure("Transaction would exceed months's usage")
    elif at.exceeds_yearly_limit(amount):
        retval = Result.Failure("Transaction would exceed annual usage")
    elif at.exceeds_max_balance(amount):
        retval = Result.Failure("Transaction would exceed maximum balance")
    else:
        retval = braintree_transaction(params)
    return retval


def braintree_transaction(params):
    # NOTE: this is very slow, should really kick off to a job
    amount = params.amount.amount
    result = braintree.Transaction.sale({
        "amount": amount,
        "payment_method_nonce": params.nonce,
        "options": {
          "submit_for_settlement": True
        }
    })
    if result.is_success:
        db.new_transaction(params.session, params.user_id,
                           amount, params.account_id)
        retval = Result.Success("Added {}".format(amount))
    else:
        retval = Result.Failure("Payment error: {}".format(result.message))
    return retval

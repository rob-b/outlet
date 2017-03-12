import os
import decimal
import datetime
from sqlalchemy import (create_engine, Column, Integer, DateTime, String,
                        Numeric, ForeignKey)
from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


# - maximum £500 worth of loads per day
# - maximum £800 worth of loads per 30 days
# - maximum £2000 worth of loads per 365 days
# - maximum balance at any time £1000


class AccountTransactions:
    # strictly speaking the first two limits are not yearly and monthly
    YEARLY_LIMIT = (365, 2000)
    MONTHLY_LIMIT = (30, 800)
    DAILY_LIMIT = (0, 500)
    MAX_BALANCE = 1000

    def __init__(self, session, account_id):
        self.account_id = account_id
        self.session = session
        self._account = None

    def exceeds_daily_limit(self, money):
        return self.check_limit(money, self.DAILY_LIMIT)

    def exceeds_monthly_limit(self, money):
        return self.check_limit(money, self.MONTHLY_LIMIT)

    def exceeds_yearly_limit(self, money):
        return self.check_limit(money, self.YEARLY_LIMIT)

    def exceeds_max_balance(self, money):
        total = self.total() + money.amount
        return not (decimal.Decimal(1000) >= total > decimal.Decimal(-1))

    def check_limit(self, money, limit):
        days, value = limit
        return self.for_days(days) >= (value - money.amount)

    def for_days(self, days=0):
        dt = datetime.datetime.utcnow()
        start_date = (dt - datetime.timedelta(days=days)).date()
        return transactions_for_account(self.session,
                                        self.account_id, start_date)

    def total(self):
        if self._account is None:
            q = (self.session.query(Account)
                 .filter(Account.id == self.account_id))
            self._account = q.one()
        return self._account.amount


def get_total(session, account_id):
    inner = func.coalesce(func.sum(Transaction.amount), 0)
    return (session
            .query(inner)
            .filter(Transaction.account_id == account_id)
            .scalar())


def transactions_for_account(session, account_id, start_date=None):
    inner = func.coalesce(func.sum(Transaction.amount), 0)
    query = session.query(inner).filter(Transaction.account_id == account_id,
                                        Transaction.amount > 0)
    if start_date is None:
        start_date = datetime.datetime.utcnow().date()
    return query.filter(Transaction.created > start_date).scalar()


def new_transaction(session, user_id, amount, account_id):
    trans = Transaction(user_id=user_id, amount=amount, account_id=account_id)
    session.add(trans)
    account = session.query(Account).filter(Account.id == account_id).one()
    account.amount = account.amount + amount


def new_account(session):
    account = Account(amount=0, user_id=1001)
    session.add(account)
    return account


def make_engine():
    db_uri = os.environ['DB_URL']
    return create_engine(db_uri, echo=True)


def make_session():
    engine = make_engine()
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def make_db():
    Base.metadata.create_all(make_engine())
    session = make_session()
    new_account(session)
    session.commit()


Base = declarative_base()
Session = make_session()


class Transaction(Base):
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False, default=0)
    currency = Column(String, nullable=False, default='GBP')
    exchange_rate = Column(Numeric, nullable=False, default='1.0')
    user_id = Column(Integer, nullable=False)
    account_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    account = relationship("Account")
    created = Column(DateTime, nullable=False, default=func.now())


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    amount = Column(Numeric, nullable=False, default=0)
    user_id = Column(Integer, nullable=False)

    def __json__(self):
        return {'amount': self.amount}

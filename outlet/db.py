import datetime
from sqlalchemy import (create_engine, Column, Integer, DateTime, String,
                        Numeric, ForeignKey)
from sqlalchemy.sql import func
from sqlalchemy.orm import scoped_session, sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base


class UserTransactions:
    def __init__(self, session, user_id):
        self.user_id = user_id
        self.session = session

    def for_days(self, days=0):
        dt = datetime.datetime.utcnow()
        start_date = (dt - datetime.timedelta(days=days)).date()
        return transactions_for_user(self.session, self.user_id, start_date)

    def total(self):
        # NOTE: this is obviously not scalable and so a running total should be
        # stored in its own table and calculated after every transaction
        inner = func.coalesce(func.sum(Transaction.amount), 0)
        return (self.session
                .query(inner)
                .filter(Transaction.user_id == self.user_id)
                .scalar())


def transactions_for_user(session, user_id, start_date=None):
    inner = func.coalesce(func.sum(Transaction.amount), 0)
    query = session.query(inner).filter(Transaction.user_id == user_id,
                                        Transaction.amount > 0)
    if start_date is None:
        start_date = datetime.datetime.utcnow().date()
    return query.filter(Transaction.created > start_date).scalar()


def new_transaction(user_id, amount, account_id):
    return Transaction(user_id=user_id, amount=amount, account_id=account_id)


def make_engine():
    db_uri = 'sqlite:///balances.db'
    db_uri = 'postgresql://game@/outlet'
    return create_engine(db_uri, echo=True)


def make_session():
    engine = make_engine()
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)


def make_db():
    Base.metadata.create_all(make_engine())
    session = make_session()
    session.add(Account(amount=0, user_id=1001))
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
    amount = Column(Integer, nullable=False, default=0)
    user_id = Column(Integer, nullable=False)

    def __json__(self):
        return {'amount': self.amount}

from sqlalchemy import Column, String, Integer, desc

from app.models.base import Base
from app.models.base import session_scope


class User(Base):
    __tablename__ = 'users'  # テーブル名
    user_id = Column(Integer, primary_key=True, unique=True)  # primary_key
    screen_name = Column(String)  # apissQX70のような目に見えるid
    latest_checked_tweet = Column(Integer)  # 取得済みの最新ツイートid
    threshold = Column(Integer)  # RT数のしきい値

    def __repr__(self):
        return f"UserObject<id={self.user_id}>"

    def save(self):
        with session_scope() as session:
            session.add(self)

    @classmethod
    def update_latest_tweet(self, user_id, tweet_id):
        with session_scope() as session:
            user = session.query(User).filter(User.user_id == user_id).all()
            user.latest_checked_tweet = tweet_id

    @classmethod
    def update_threshold(self, user_id, threshold):
        with session_scope() as session:
            user = session.query(User).filter(User.user_id == user_id).all()
            user.threshold = threshold

    @classmethod
    def get_users(cls, limit=10):
        with session_scope() as session:
            users = session.query(cls).order_by(
                desc(cls.user_id)).limit(limit).all()
        if users is None:
            return None
        else:
            return users

    @classmethod
    def delete_user(cls, screen_name):
        with session_scope() as session:
            user = session.query(User).filter(
                User.screen_name == screen_name).all()
            if user is None or len(user) != 1:
                return False
            else:
                session.delete(user[0])
                return True

    @classmethod
    def get_user(cls, screen_name):
        with session_scope() as session:
            user = session.query(User).filter(
                User.screen_name == screen_name).all()
        if user is None or len(user) != 1:
            return None
        else:
            return user[0]

from contextlib import contextmanager
import threading
import logging

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session

logger = logging.getLogger(__name__)
Base = declarative_base()  # データベースのテーブルの親
engine = create_engine('sqlite:///user.db')  # user.db というデータベースを使う宣言
Session = scoped_session(sessionmaker(bind=engine))
lock = threading.Lock()


def init_db():
    import app.models.user
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope():
    session = Session()
    session.expire_on_commit = False
    try:
        lock.acquire()
        yield session
        session.commit()
    except Exception as e:
        logger.error(f'action=session_scope error={e}')
        session.rollback()
        raise
    finally:
        session.expire_on_commit = True
        lock.release()

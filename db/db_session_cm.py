from contextlib import contextmanager
from sqlalchemy.orm import Session

from db.session import get_session_factory, get_async_session_factory


@contextmanager
def db_session():
    session = get_session_factory()()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

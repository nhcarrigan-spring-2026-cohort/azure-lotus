from core.setting import Settings
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session
from ..main import app


from sqlmodel import Session, create_engine

engine = create_engine(Settings.DATABASE_TEST_URL, echo=True)


def get_session():
    with Session(engine) as session:
        yield session
        
@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def db():
    session = Session(engine)
    try:
        yield session
        session.commit()  # Commit changes so they can be observed in tests
    finally:
        session.rollback()
        session.close()

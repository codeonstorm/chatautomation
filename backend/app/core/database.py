from sqlmodel import SQLModel, create_engine, Session

from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    # connect_args={"check_same_thread": False}  # Only needed for SQLite
)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

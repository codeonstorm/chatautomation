# Define MySQL connection URL
DATABASE_URL = "mysql+mysqlconnector://root:@localhost:3306/chatbot"
from sqlmodel import SQLModel, Field, Session, create_engine, select
from typing import Optional

# Create a MySQL engine
engine = create_engine(DATABASE_URL, echo=True)

# Define a table/model
class Hero(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    age: Optional[int] = None

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Insert a new hero into the database
def create_hero():
    hero = Hero(name="Iron Man", age=45)
    with Session(engine) as session:
        session.add(hero)
        session.commit()
        session.refresh(hero)
    print(f"Created Hero: {hero}")

# Retrieve all heroes
def get_heroes():
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement).all()
        for hero in results:
            print(hero)

# Run the setup
if __name__ == "__main__":
    create_db_and_tables()  # Create tables
    create_hero()  # Insert data
    get_heroes()  # Query data

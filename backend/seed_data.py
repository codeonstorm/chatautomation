from dotenv import load_dotenv
import os

from sqlmodel import SQLModel, Session, create_engine
from app.models.models import Plan
from app.schemas.enums import *

def seed_plans(session):
  plans = [
    Plan(name="Free", description="Basic free plan", price=0.0, billing_cycle="monthly", status=StatusEnum.enabled, trial_period=14, features="Limited features"),
    Plan(name="Silver", description="Affordable mid-tier plan", price=9.99, billing_cycle="monthly", status=StatusEnum.enabled, trial_period=14, features="Access to core features"),
    Plan(name="Gold", description="Advanced features for professionals", price=19.99, billing_cycle="monthly", status=StatusEnum.enabled, trial_period=14, features="Premium support, Extra tools"),
    Plan(name="Premium", description="All-inclusive plan with full features", price=49.99, billing_cycle="monthly", status=StatusEnum.enabled, trial_period=14, features="Everything unlimited"),
  ]

  for plan in plans:
    existing_plan = session.get(Plan, plan.name)
    if not existing_plan:
      session.add(plan)

    session.commit()

load_dotenv()
DATABASE_URL: str = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def create_db_and_seed():
  # SQLModel.metadata.create_all(engine)
  with Session(engine) as session:
      seed_plans(session)

if __name__ == "__main__":
  create_db_and_seed()

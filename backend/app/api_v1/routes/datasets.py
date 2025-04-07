from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session

from app.models.dataset import Dataset
from app.schemas.response import ResponseSchema
from app.schemas.dataset import DatasetRead, DatasetUpdate

router = APIRouter(prefix="/{service_id}/datasets", tags=["datasets"])


@router.get("", response_model=list[DatasetRead])
def get_datasets(
    *,
    service_id: int,
    db: Session = Depends(get_session),
) -> List[DatasetRead]:
    plans = db.exec(select(Dataset).where(Dataset.service_id == service_id)).all()
    if not plans:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No datasets found."
        )
    return plans


@router.put("/{dataset_id}", response_model=ResponseSchema)
def update_dataset(
    *,
    service_id: int,
    dataset_id: int,
    update_in: DatasetUpdate,
    session: Session = Depends(get_session),
):
    dataset = session.exec(
        select(Dataset).where(
            Dataset.service_id == service_id, Dataset.id == dataset_id
        )
    ).first()

    if not dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset_data = update_in.dict(exclude_unset=True)
    for key, value in dataset_data.items():
        setattr(dataset, key, value)

    session.add(dataset)
    session.commit()
    session.refresh(dataset)

    return ResponseSchema(
        success=True,
        message="Dataset updated successfully",
    )

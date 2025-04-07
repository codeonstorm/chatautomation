from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.item import Item
from app.schemas.item import ItemCreate, ItemUpdate


class ItemService:
    def get_item(self, db: Session, item_id: int) -> Optional[Item]:
        return db.query(Item).filter(Item.id == item_id).first()

    def get_items(self, db: Session, skip: int = 0, limit: int = 100) -> List[Item]:
        return db.query(Item).offset(skip).limit(limit).all()

    def get_user_items(
        self, db: Session, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Item]:
        return (
            db.query(Item)
            .filter(Item.owner_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_item(self, db: Session, item: ItemCreate) -> Item:
        db_item = Item(
            title=item.title, description=item.description, owner_id=item.owner_id
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def update_item(self, db: Session, item_id: int, item: ItemUpdate) -> Item:
        db_item = self.get_item(db, item_id)
        update_data = item.dict(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_item, key, value)

        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    def delete_item(self, db: Session, item_id: int) -> None:
        db_item = self.get_item(db, item_id)
        db.delete(db_item)
        db.commit()

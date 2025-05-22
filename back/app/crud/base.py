from typing import TypeVar, Type, List, Optional
from sqlalchemy.orm import Session
from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError

T = TypeVar("T")


def create_obj(db: Session, obj_in: T) -> T:
    try:
        db.add(obj_in)
        db.commit()
        db.refresh(obj_in)
        return obj_in
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


def get_obj_by_id(db: Session, model: Type[T], obj_id: int) -> T:
    obj = db.query(model).get(obj_id)
    if not obj:
        raise HTTPException(status_code=404, detail=f"{model.__name__} with id={obj_id} not found")
    return obj


def get_obj_by_field(db: Session, model: Type[T], field_name: str, value: str) -> Optional[T]:
    field = getattr(model, field_name, None)
    if field is None:
        raise HTTPException(status_code=400, detail=f"Field '{field_name}' not found in model {model.__name__}")

    obj = db.query(model).filter(field == value).first()
    return obj


def update_obj(db: Session, model: Type[T], obj_id: int, updates: dict) -> T:
    db_obj = get_obj_by_id(db, model, obj_id)
    for key, value in updates.items():
        setattr(db_obj, key, value)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete_obj(db: Session, model: Type[T], obj_id: int) -> bool:
    try:
        deleted = db.query(model).filter(model.id == obj_id).delete()
        if deleted == 0:
            raise HTTPException(status_code=404, detail=f"{model.__name__} with id={obj_id} not found")
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")



def list_all(db: Session, model: Type[T], limit: int = 100) -> List[T]:
    return db.query(model).limit(limit).all()
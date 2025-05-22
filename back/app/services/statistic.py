from datetime import datetime

from sqlalchemy.orm import Session
from fastapi import HTTPException
from back.app.models.pg_data import Dialog, Message, Rating
from back.app.crud.base import create_obj, get_obj_by_id, update_obj, delete_obj
from typing import List, Type


class DialogService:
    def __init__(self, db: Session):
        self.db = db

    def start_dialog(self, dialog_data: Dialog) -> int:

        return create_obj(self.db, dialog_data).dialog_id

    def end_dialog(self, dialog_id: int):
        dialog = get_obj_by_id(self.db, Dialog, dialog_id)
        if not dialog:
            raise HTTPException(status_code=404, detail="Dialog not found")
        dialog.status = "closed"
        dialog.ended_at = datetime.utcnow()
        self.db.commit()

    def get_user_dialogs(self, user_id: int) -> list[Type[Dialog]]:
        return self.db.query(Dialog).filter_by(user_id=user_id).order_by(Dialog.started_at.desc()).all()

    def get_active_dialog_by_username(self, username: str) -> Type[Dialog] | None:
        return self.db.query(Dialog).filter_by(user_name=username, status="active").order_by(Dialog.started_at.desc()).first()

class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def add_message(self, message_data: Message):
        create_obj(self.db, message_data)

    def get_dialog_messages(self, dialog_id: int) -> list[Type[Message]]:
        return self.db.query(Message).filter_by(dialog_id=dialog_id).order_by(Message.sent_at).all()

class RatingService:
    def __init__(self, db: Session):
        self.db = db

    def add_rating(self, rating_data: Rating):
        create_obj(self.db, rating_data)
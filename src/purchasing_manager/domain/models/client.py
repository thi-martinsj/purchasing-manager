from datetime import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP, UUID

from purchasing_manager import db


class Client(db.Model):
    __tablename__ = "client"

    id = db.Column(UUID(as_uuid=True), primary_key=True)
    created_dt = db.Column(TIMESTAMP(timezone=True), default=datetime.now(), nullable=False)
    updated_dt = db.Column(TIMESTAMP(timezone=True), default=datetime.now(), onupdate=datetime.now(), nullable=False)
    name = db.Column(db.String(50), nullable=False, index=True)
    document = db.Column(db.String(11), nullable=False, index=True)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(50), nullable=False)

    @property
    def dict(self):
        return {
            "id": str(self.id),
            "created_dt": str(self.created_dt),
            "updated_dt": str(self.updated_dt),
            "name": self.name,
            "document": self.document,
            "phone": self.phone,
            "email": self.email,
        }

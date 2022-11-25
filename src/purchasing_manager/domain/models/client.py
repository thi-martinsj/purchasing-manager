from sqlalchemy.dialects.postgresql import UUID

from purchasing_manager import db


class Client(db.Model):
    id = db.Column(UUID(as_uuid=True), primary_key=True)
    name = db.Column(db.String(50), nullable=False, index=True)
    document = db.Column(db.String(11), nullable=False, index=True)
    phone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(30), nullable=False)

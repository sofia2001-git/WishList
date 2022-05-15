from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean
)
from ..database import db
from sqlalchemy_serializer import SerializerMixin


class Wish(db.Model, SerializerMixin):
    __tablename__ = 'wishes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    image = Column(String, nullable=True)
    link = Column(String, nullable=True)
    description = Column(String(250), nullable=True)
    is_private = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"<Wish {self.title[:self.title.index(' ')]}>"

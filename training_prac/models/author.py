
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class Author(BaseModel):
    __tablename__ = "authors"

    author_id: Mapped[int] = mapped_column(primary_key=True)

    name_author: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)

    books: Mapped[list['Book']] = relationship(back_populates='author')

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class Genre(BaseModel):
    __tablename__ = "genres"

    genre_id: Mapped[int] = mapped_column(primary_key=True)

    name_genre: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    books: Mapped[list['Book']] = relationship(back_populates='genre')

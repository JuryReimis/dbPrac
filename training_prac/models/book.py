
from decimal import Decimal

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from training_prac.models.database import BaseModel


class Book(BaseModel):
    __tablename__ = "books"

    book_id: Mapped[int] = mapped_column(primary_key=True)

    title: Mapped[str] = mapped_column(String(255))

    author_id: Mapped[int] = mapped_column(ForeignKey('authors.author_id', ondelete="CASCADE"), index=True)

    author: Mapped['Author'] = relationship(back_populates='books')

    genre_id: Mapped[int | None] = mapped_column(ForeignKey('genres.genre_id', ondelete="SET NULL"), index=True)

    genre: Mapped['Genre | None'] = relationship(back_populates='books')

    price: Mapped[Decimal] = mapped_column()

    amount: Mapped[int] = mapped_column()

    buy: Mapped[list['Buy']] = relationship(back_populates='bought_books', secondary="buy_books")

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from training_prac.models.database import BaseModel


class BuyBook(BaseModel):
    __tablename__ = "buy_books"

    buy_book_id: Mapped[int] = mapped_column(primary_key=True)

    buy_id: Mapped[int] = mapped_column(ForeignKey('buy.buy_id', ondelete="CASCADE"))

    book_id: Mapped[int] = mapped_column(ForeignKey('books.book_id', ondelete="CASCADE"))

    amount: Mapped[int] = mapped_column()

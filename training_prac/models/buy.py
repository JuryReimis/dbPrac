from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class Buy(BaseModel):
    __tablename__ = "buy"

    buy_id: Mapped[int] = mapped_column(primary_key=True)

    buy_description: Mapped[str | None] = mapped_column(String(1000))

    client_id: Mapped[int] = mapped_column(ForeignKey('clients.client_id', ondelete="CASCADE"), index=True)

    client: Mapped['Client'] = relationship(back_populates='buy')

    bought_books: Mapped[list['Book']] = relationship(back_populates='buy', secondary="buy_books")

    step: Mapped['Step'] = relationship(back_populates='buy', secondary='buy_steps')

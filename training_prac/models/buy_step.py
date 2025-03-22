from datetime import datetime

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class BuyStep(BaseModel):
    __tablename__ = "buy_steps"

    buy_step_id: Mapped[int] = mapped_column(primary_key=True)

    buy_id: Mapped[int] = mapped_column(ForeignKey('buy.buy_id', ondelete="CASCADE"))

    step_id: Mapped[int | None] = mapped_column(ForeignKey('steps.step_id', ondelete="SET NULL"))

    date_step_beg: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    date_step_end: Mapped[datetime] = mapped_column(DateTime, nullable=True)

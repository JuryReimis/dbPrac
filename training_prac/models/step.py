from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class Step(BaseModel):
    __tablename__ = "steps"

    step_id: Mapped[int] = mapped_column(primary_key=True)

    name_step: Mapped[str] = mapped_column(String(510), unique=True, index=True)

    buy: Mapped[list['Buy']] = relationship(back_populates='step', secondary='buy_steps')

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class City(BaseModel):
    __tablename__ = "cities"

    city_id: Mapped[int] = mapped_column(primary_key=True)

    name_city: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, index=True)

    days_delivery: Mapped[int] = mapped_column()

    clients: Mapped[list['Client']] = relationship(back_populates='city')

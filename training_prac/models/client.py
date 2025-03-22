from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from training_prac.models.database import BaseModel


class Client(BaseModel):
    __tablename__ = "clients"

    client_id: Mapped[int] = mapped_column(primary_key=True)

    name_client: Mapped[str] = mapped_column(String(255), index=True)

    city_id: Mapped[int] = mapped_column(ForeignKey('cities.city_id'))

    city: Mapped['City'] = relationship(back_populates='clients')

    email: Mapped[str] = mapped_column(unique=True)

    buy: Mapped[list['Buy']] = relationship(back_populates='client')

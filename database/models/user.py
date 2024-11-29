from email.policy import default

import datetime
#from pip._internal.utils import datetime
from sqlalchemy import Column, String, Integer, Boolean, Numeric, DateTime, BLOB, func
from sqlalchemy.dialects.mysql import DATETIME
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.testing.schema import mapped_column


class Base(DeclarativeBase):
    created:Mapped[DATETIME]= mapped_column(DATETIME , default=func.now())
    updated: Mapped[DATETIME]= mapped_column(DATETIME , default=func.now() , onupdate=func.now())



class User(Base):
    __tablename__ = 'user'

    id: Mapped[int] = mapped_column(Integer, primary_key = True, autoincrement = True)
    name: Mapped[str] = mapped_column(String(150), nullable = False)
    status_subscription: Mapped[bool] = mapped_column(String(50), nullable = True)  # Use String for subscription status
    balance: Mapped[float] = mapped_column(Numeric(10, 2), nullable = False, default = 0.00)  # Use Numeric for monetary values
    image: Mapped[bytes] = mapped_column(BLOB(), nullable = True)
    date: Mapped[datetime.datetime] = mapped_column(DateTime, default = datetime.datetime.now(datetime.timezone.utc))

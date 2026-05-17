from sqlalchemy import Column, Integer, String, Date
from app.database import Base


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False)
    city = Column(String, nullable=False)

    aqi = Column(Integer, nullable=False)
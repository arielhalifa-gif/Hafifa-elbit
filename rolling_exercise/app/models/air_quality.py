from sqlalchemy import Column, Integer, String, Float, Date
from app.database import Base


class AirQuality(Base):
    __tablename__ = "air_quality"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False)
    city = Column(String, nullable=False)

    pm25 = Column(Float, nullable=False)
    no2 = Column(Float, nullable=False)
    co2 = Column(Float, nullable=False)

    aqi = Column(Integer, nullable=False)
    aqi_level = Column(String, nullable=False)
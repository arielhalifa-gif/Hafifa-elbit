from app.database import engine, Base

from app.models.air_quality import AirQuality
from app.models.alert import Alert

Base.metadata.create_all(bind=engine)

print("Tables created successfully")
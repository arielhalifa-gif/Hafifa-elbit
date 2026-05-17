import os
import shutil

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.database import get_db

from app.models.air_quality import AirQuality
from app.models.alert import Alert

from app.services.csv_processor import process_csv

from app.utils.logger import logger

router = APIRouter()


@router.post("/upload")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    if not file.filename.endswith(".csv"):

        raise HTTPException(
            status_code=400,
            detail="Only CSV files are allowed"
        )

    file_location = f"air_quality_files/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    logger.info(f"File uploaded: {file.filename}")

    result = process_csv(file_location, db)

    return {
        "message": "File processed successfully",
        "result": result
    }


@router.get("/air-quality")
def get_air_quality(
    start_date: str,
    end_date: str,
    db: Session = Depends(get_db)
):

    data = db.query(AirQuality).filter(
        AirQuality.date >= start_date,
        AirQuality.date <= end_date
    ).all()

    return data


@router.get("/air-quality/city")
def get_city_data(
    city: str,
    db: Session = Depends(get_db)
):

    data = db.query(AirQuality).filter(
        AirQuality.city == city
    ).all()

    return data


@router.get("/aqi-history")
def get_aqi_history(
    city: str,
    db: Session = Depends(get_db)
):

    data = db.query(
        AirQuality.date,
        AirQuality.aqi,
        AirQuality.aqi_level
    ).filter(
        AirQuality.city == city
    ).all()

    return data


@router.get("/aqi-average")
def get_average_aqi(
    city: str,
    db: Session = Depends(get_db)
):

    avg = db.query(
        func.avg(AirQuality.aqi)
    ).filter(
        AirQuality.city == city
    ).scalar()

    return {
        "city": city,
        "average_aqi": round(avg, 2)
    }


@router.get("/best-cities")
def get_best_cities(
    db: Session = Depends(get_db)
):

    data = db.query(
        AirQuality.city,
        func.avg(AirQuality.aqi).label("avg_aqi")
    ).group_by(
        AirQuality.city
    ).order_by(
        func.avg(AirQuality.aqi)
    ).limit(3).all()

    return data


@router.get("/alerts")
def get_alerts(
    db: Session = Depends(get_db)
):

    return db.query(Alert).all()


@router.get("/alerts/date")
def get_alerts_by_date(
    date: str,
    db: Session = Depends(get_db)
):

    return db.query(Alert).filter(
        Alert.date == date
    ).all()


@router.get("/alerts/city")
def get_alerts_by_city(
    city: str,
    db: Session = Depends(get_db)
):

    return db.query(Alert).filter(
        Alert.city == city
    ).all()
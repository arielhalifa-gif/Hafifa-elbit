import pandas as pd

from datetime import datetime

from app.models.air_quality import AirQuality
from app.models.alert import Alert

from app.services.validator import validate_row
from app.services.aqi_service import generate_aqi

from app.utils.logger import logger


def process_csv(file_path, db):

    df = pd.read_csv(file_path)

    inserted_rows = 0
    invalid_rows = 0

    for _, row in df.iterrows():

        row_data = row.to_dict()

        if not validate_row(row_data):

            logger.error(f"Invalid row ignored: {row_data}")

            invalid_rows += 1
            continue

        aqi, level = generate_aqi(
            row_data["pm25"],
            row_data["no2"],
            row_data["co2"]
        )

        air_quality = AirQuality(
            date=datetime.strptime(
                row_data["date"],
                "%Y-%m-%d"
            ).date(),

            city=row_data["city"],

            pm25=row_data["pm25"],
            no2=row_data["no2"],
            co2=row_data["co2"],

            aqi=aqi,
            aqi_level=level
        )

        db.add(air_quality)

        if aqi > 300:

            alert = Alert(
                date=datetime.strptime(
                    row_data["date"],
                    "%Y-%m-%d"
                ).date(),

                city=row_data["city"],
                aqi=aqi
            )

            db.add(alert)

            logger.warning(
                f"ALERT CREATED - City: {row_data['city']} AQI: {aqi}"
            )

        inserted_rows += 1

    db.commit()

    logger.info(
        f"CSV processed successfully. "
        f"Inserted: {inserted_rows}, "
        f"Invalid: {invalid_rows}"
    )

    return {
        "inserted_rows": inserted_rows,
        "invalid_rows": invalid_rows
    }
from datetime import datetime


def validate_row(row):

    required_fields = [
        "date",
        "city",
        "pm25",
        "no2",
        "co2"
    ]

    for field in required_fields:
        if field not in row:
            return False

        if row[field] is None:
            return False

    try:
        datetime.strptime(str(row["date"]), "%Y-%m-%d")

        if float(row["pm25"]) < 0:
            return False

        if float(row["no2"]) < 0:
            return False

        if float(row["co2"]) < 0:
            return False

    except Exception:
        return False

    return True
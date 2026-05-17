from app.services.validator import validate_row


def test_valid_row():

    row = {
        "date": "2025-01-01",
        "city": "Haifa",
        "pm25": 10,
        "no2": 20,
        "co2": 100
    }

    assert validate_row(row) is True


def test_invalid_row():

    row = {
        "city": "Haifa"
    }

    assert validate_row(row) is False
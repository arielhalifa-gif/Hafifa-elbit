from app.services.aqi_service import generate_aqi


def test_generate_aqi():

    aqi, level = generate_aqi(
        10,
        20,
        100
    )

    assert aqi >= 0
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_upload_invalid_file():

    response = client.post(
        "/upload",
        files={"file": ("test.txt", b"hello")}
    )

    assert response.status_code == 400
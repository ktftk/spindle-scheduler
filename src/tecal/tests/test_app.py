from dataclasses import dataclass

from fastapi.testclient import TestClient

from app.main import app, get_repository


@dataclass
class MockRepository:
    def upload_raw_calendar(self, *args, **kwargs) -> None:
        pass

    def upload_parsed_calendar(self, *args, **kwargs) -> None:
        pass


client = TestClient(app)


app.dependency_overrides[get_repository] = lambda: MockRepository()


def test_scrape() -> None:
    response = client.post("/v1/scrape")
    assert response.status_code == 200

import logging
import os
from datetime import date, timedelta
from pathlib import Path
from typing import Annotated
from uuid import UUID

from fastapi import Depends, FastAPI, status
from pydantic import BaseModel

from .download import download
from .parse import parse
from .repository import Repository
from .services import generate_scrape_id

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CompletedScrape(BaseModel):
    id: UUID
    start: date
    end: date


app = FastAPI()


def get_repository() -> Repository:
    return Repository(bucket_name=os.environ["GCS_BUCKET_NAME"])


def raw_calender_dir() -> Path:
    return Path(os.getenv("RAW_CALENDAR_PATH", "./data/raw"))


def parsed_calender_dir() -> Path:
    return Path(os.getenv("PRASED_CALENDAR_DIR", "./data/parsed"))


@app.post(
    "/v1/scrape",
    status_code=status.HTTP_200_OK,
    operation_id="scrape",
    response_model=CompletedScrape,
)
async def scrape(
    repository: Annotated[Repository, Depends(get_repository)],
    raw_calender_dir: Annotated[Path, Depends(raw_calender_dir)],
    parsed_calender_dir: Annotated[Path, Depends(parsed_calender_dir)],
) -> CompletedScrape:
    scrape_id = generate_scrape_id()
    logger.info(f"Scrape ID: {scrape_id}")

    date_range_before = int(os.getenv("DATE_RANGE_BEFORE", "7"))
    date_range_after = int(os.getenv("DATE_RANGE_AFTER", "45"))
    start = date.today() - timedelta(days=date_range_before)
    end = date.today() + timedelta(days=date_range_after)

    raw_calender_dir.mkdir(parents=True, exist_ok=True)
    raw_calendar_path = raw_calender_dir / f"{scrape_id}.html"
    await download(raw_calendar_path, start, end)
    repository.upload_raw_calendar(scrape_id, raw_calendar_path)

    forward_date_days = int(os.getenv("FORWARD_DATE_DAYS", "45"))
    forward_date = date.today() + timedelta(days=forward_date_days)

    parsed_calender_dir.mkdir(parents=True, exist_ok=True)
    parsed_calender_path = parsed_calender_dir / f"{scrape_id}.csv"
    parse(raw_calendar_path, parsed_calender_path, forward_date)
    repository.upload_parsed_calendar(scrape_id, parsed_calender_path)

    return CompletedScrape(id=scrape_id, start=start, end=end)

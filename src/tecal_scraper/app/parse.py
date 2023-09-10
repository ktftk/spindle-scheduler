import logging
import re
from datetime import date, datetime
from pathlib import Path

import bs4
import pandas as pd
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def is_header_row(tr: bs4.element.Tag) -> bool:
    return tr.get("style") == "white-space: nowrap"


def is_data_row(tr: bs4.element.Tag) -> bool:
    return tr.get("data-id") is not None


def parse_header_row(tr: bs4.element.Tag) -> dict:
    if tr.th is None:
        raise ValueError(f"invalid element: ${tr}")
    return {"date_str": tr.th.get_text(strip=True)}


def parse_data_row(tr: bs4.element.Tag) -> dict:
    symbol = tr.get("data-symbol")
    url = tr.get("data-url")
    category = tr.get("data-category")
    event_name = tr.get("data-event")

    time_span = tr.find("span", {"class": re.compile(r"^calendar-date-\d+$")})
    time_str = (
        time_span.get_text(strip=True) if time_span is not None else None
    )

    country_code_td = tr.find("td", {"class": "calendar-iso"})
    if country_code_td is None:
        raise ValueError(f"invalid element: ${country_code_td}")
    country_code = country_code_td.get_text(strip=True)

    event_a = tr.find("a", {"class": "calendar-event"})
    event_title = event_a.get_text(strip=True) if event_a is not None else None

    reference_span = tr.find("span", {"class": "calendar-reference"})
    period_str = (
        reference_span.get_text(strip=True)
        if reference_span is not None
        else None
    )

    return {
        "symbol": symbol,
        "url": url,
        "category": category,
        "event_name": event_name,
        "event_title": event_title,
        "time_str": time_str,
        "country_code": country_code,
        "period_str": period_str,
    }


def extract(soup: BeautifulSoup) -> pd.DataFrame:
    table = soup.find(id="calendar")
    if table is None or isinstance(table, str):
        raise ValueError(f"invalid element: ${table}")
    trs = table.find_all("tr")
    records = []
    for tr in trs:
        if is_header_row(tr):
            records.append(parse_header_row(tr))
        elif is_data_row(tr):
            records.append(parse_data_row(tr))
    return pd.DataFrame(records)


def is_quarterly_period(s: str) -> bool:
    return re.match(r"^Q\d$", s) is not None


def is_monthly_period(s: str) -> bool:
    return len(s) == 3 or s == "APRIL" or s == "SEPT"


def is_weekly_period(s: str) -> bool:
    return re.match(r"^\w{3}/\d{2}$", s) is not None


def parse_month(s: str) -> int:
    if s == "SEPT":
        return 9
    if len(s) == 3:
        return datetime.strptime(s, "%b").month
    return datetime.strptime(s, "%B").month


# Combination of "country_code", "event_name", "period"
# and "datetime" is unique
def transform(df: pd.DataFrame, forward_date: date) -> pd.DataFrame:
    df["date"] = df[df["date_str"].notna()]["date_str"].apply(
        lambda x: datetime.strptime(x, "%A %B %d %Y").date()
    )
    df["date"] = df["date"].ffill()

    # Drop header row (date row)
    df = df[df["event_name"].notna()].copy()

    df["time"] = df[df["time_str"].notna()]["time_str"].apply(
        lambda x: datetime.strptime(x, "%I:%M %p").time()  # type: ignore
    )

    df["datetime"] = df[df["date"].notna() & df["time"].notna()].apply(
        lambda x: datetime.combine(x["date"], x["time"]), axis=1
    )

    month_to_year = {}
    for i in range(12):
        period = pd.Period(str(forward_date), freq="M") - i
        month_to_year[period.month] = period.year

    def parse_quarterly_period(s: str) -> pd.Period:
        start_month = (int(s[1]) - 1) * 3 + 1
        start_year = month_to_year[start_month]
        return pd.Period(str(date(start_year, start_month, 1)), freq="Q")

    def parse_monthly_period(s: str) -> pd.Period:
        month = parse_month(s)
        year = month_to_year[month]
        return pd.Period(str(date(year, month, 1)), freq="M")

    def parse_weekly_period(s: str) -> pd.Period:
        month_str, day_str = s.split("/")
        day = int(day_str)
        month = datetime.strptime(month_str, "%b").month
        year = month_to_year[month]
        d = date(year, month, day)
        weekday = d.strftime("%a").upper()
        return pd.Period(str(d), freq=f"W-{weekday}")

    def parse_period(s: str) -> pd.Period:
        if is_quarterly_period(s):
            return parse_quarterly_period(s)
        elif is_monthly_period(s):
            return parse_monthly_period(s)
        elif is_weekly_period(s):
            return parse_weekly_period(s)
        raise ValueError(f"invalid period: {s}")

    df["period"] = df[df["period_str"] != ""]["period_str"].apply(
        lambda x: parse_period(x).start_time.date()
    )

    df = df[
        [
            "country_code",
            "event_name",
            "period",
            "datetime",
            "category",
            "event_title",
            "url",
        ]
    ]

    return df


COLUMNS_FOR_UNIQUE = ["country_code", "event_name", "period", "datetime"]


def validte_unique_scheduled_release(df: pd.DataFrame) -> pd.DataFrame:
    scheduled_df = df[df["datetime"].notna()]
    duplicated = scheduled_df[scheduled_df[COLUMNS_FOR_UNIQUE].duplicated()]
    for record in duplicated.to_dict(orient="records"):
        logger.warning(f"duplicated record: {record}")
    return scheduled_df.drop_duplicates(subset=COLUMNS_FOR_UNIQUE)


def validate(df: pd.DataFrame) -> pd.DataFrame:
    df = validte_unique_scheduled_release(df)
    return df


def parse(source: str | Path, dest: str | Path, forward_date: date) -> None:
    with open(source, "r") as file:
        data = file.read()

    soup = BeautifulSoup(data, "html.parser")
    df = extract(soup)
    df = transform(df, forward_date)
    df = validate(df)

    df.to_csv(dest, index=False)

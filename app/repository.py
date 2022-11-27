import datetime

import psycopg2
import psycopg2.extras
from psycopg2._psycopg import connection

from .config import (
    DB_DBNAME,
    DB_HOST,
    DB_PASSWORD,
    DB_PORT,
    DB_USER,
    REMINDER_ADVANCE_TIME,
    REMINDER_DEADLINE_TIME,
)
from .domains import Release


def get_conn() -> connection:
    return psycopg2.connect(
        dbname=DB_DBNAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
    )


def read_releases_to_remind(conn: connection) -> list[Release]:
    start_datetime = datetime.datetime.fromtimestamp(
        datetime.datetime.utcnow().timestamp() - REMINDER_DEADLINE_TIME
    )
    end_datetime = datetime.datetime.fromtimestamp(
        datetime.datetime.utcnow().timestamp() + REMINDER_ADVANCE_TIME
    )
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(
        """
            WITH "release" AS (
                SELECT
                    "release".*,
                    "release_reminder"."id" AS "release_reminder_id"
                FROM
                    "spinner"."release"
                LEFT JOIN "spinner"."release_reminder"
                    ON "release"."gen_id" = "release_reminder"."release_gen_id"
            )
            SELECT
                "gen_id",
                "id",
                "group_code",
                "dataset_code",
                "frequency",
                "edition_period_start_date",
                "scheduled_datetime"
            FROM
                "release"
            WHERE
                "release_reminder_id" IS NULL
                AND "scheduled_datetime" >= %s
                AND "scheduled_datetime" < %s
        """,
        (start_datetime, end_datetime),
    )
    return [Release.parse_obj(record) for record in cur.fetchall()]

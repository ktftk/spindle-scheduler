from psycopg import Cursor

from ...domains import SpiderRunTask


def read_executable_spider_run_tasks(
    curosr: Cursor, advance_time: int, deadline_time: int
) -> list[SpiderRunTask]:
    curosr.execute(
        """
            WITH "executable_spider_run_task" AS (
                SELECT
                    "id",
                    "spider_name",
                    "metadata",
                    "scheduled_datetime",
                    "created_at"
                FROM
                    "spindle_scheduler_marts"."int_unexecuted_spider_run_task"
                WHERE
                    "scheduled_datetime"
                        >= current_timestamp - interval '%s seconds'
                    AND "scheduled_datetime"
                        <= current_timestamp + interval '%s seconds'
            )

            SELECT
                *
            FROM
                "executable_spider_run_task" AS "spider_run_task"
        """,
        (deadline_time, advance_time),
    )
    return [SpiderRunTask.parse_obj(record) for record in curosr.fetchall()]

import logging

import psycopg
from fastapi import Depends, FastAPI, status
from fastapi.responses import JSONResponse
from psycopg import Cursor

from spindle_scheduler.config import (
    DB_URL,
    SPIDER_RUN_TASK_EXECUTION_ADVANCE_TIME,
    SPIDER_RUN_TASK_EXECUTION_DEADLINE_TIME,
)
from spindle_scheduler.features.spider_run_task_executor import (
    SpiderRunTask,
    create_executed_spider_run_tasks,
    read_executable_spider_run_tasks,
)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

app = FastAPI()


def get_cursor():
    conn = psycopg.connect(DB_URL)
    cursor = conn.cursor()
    return cursor


@app.post("/execute-spider-run-tasks", response_model=list[SpiderRunTask])
def execute_spider_run_tasks(cursor: Cursor = Depends(get_cursor)):
    spider_run_tasks = read_executable_spider_run_tasks(
        cursor,
        advance_time=SPIDER_RUN_TASK_EXECUTION_ADVANCE_TIME,
        deadline_time=SPIDER_RUN_TASK_EXECUTION_DEADLINE_TIME,
    )
    create_executed_spider_run_tasks(cursor, spider_run_tasks)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=spider_run_tasks,
    )

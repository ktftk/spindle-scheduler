import json
from datetime import datetime

import pandas as pd
import pytest

from prisma import Json, Prisma

from .config import SPIDER_RUN_TASK_PATH


@pytest.fixture(scope="module", autouse=True)
def insert_mock_records():
    df = pd.read_csv(SPIDER_RUN_TASK_PATH, dtype=str, na_values=[""])
    df = df.where(df.notna(), None)

    with Prisma() as db:
        db.spiderruntask.delete_many(where={})
        db.invokedspiderruntask.delete_many(where={})

    with Prisma() as db:
        db.spiderruntask.create_many(
            data=[
                {
                    "hash": record["hash"],
                    "spider_run_rule_id": record["spider_run_rule_id"],
                    "spider_name": record["spider_name"],
                    "release_group_code": record["release_group_code"],
                    "invoke_delay": int(record["invoke_delay"])
                    if record["invoke_delay"] is not None
                    else None,
                    "input_params": Json(json.loads(record["input_params"]))
                    if record["input_params"] is not None
                    else Json(None),
                    "target_period": datetime.fromisoformat(
                        record["target_period"]
                    ),
                    "release_period": datetime.fromisoformat(
                        record["release_period"]
                    ),
                    "release_scheduled_at": datetime.fromisoformat(
                        record["release_scheduled_at"]
                    ),
                    "scheduled_at": datetime.fromisoformat(
                        record["scheduled_at"]
                    ),
                }
                for record in df.to_dict("records")
            ]
        )

    yield

    with Prisma() as db:
        db.spiderruntask.delete_many(where={})
        db.invokedspiderruntask.delete_many(where={})

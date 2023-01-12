from __future__ import annotations

import datetime
import uuid

from psycopg import Cursor

from spindle_scheduler.config import DB_SCHEMA

from ...domains import ContextLoad as AppContextLoad
from .core import RecordBase, crete


class ContextLoad(RecordBase):
    _schema = DB_SCHEMA
    _tablename = "context_load"
    id: uuid.UUID
    created_at: datetime.datetime

    @classmethod
    def create(cls, context_load: AppContextLoad) -> ContextLoad:
        return cls(id=context_load.id, created_at=context_load.created_at)


def create_context_load(
    cursor: Cursor, context_load: AppContextLoad
) -> AppContextLoad:
    crete(cursor, ContextLoad.create(context_load))
    return context_load

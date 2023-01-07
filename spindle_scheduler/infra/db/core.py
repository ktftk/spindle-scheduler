from typing import ClassVar, TypeVar

from psycopg import Cursor, sql
from pydantic import BaseModel, PrivateAttr


class RecordBase(BaseModel):
    _schema: ClassVar[str] = PrivateAttr()
    _tablename: ClassVar[str] = PrivateAttr()

    def get_schema(self) -> str:
        return self._schema

    def get_tablename(self) -> str:
        return self._tablename

    def get_fieldnames(self) -> list[str]:
        return list(self.dict().keys())

    def get_values(self) -> list:
        return list(self.dict().values())


T = TypeVar("T", bound=RecordBase)


def crete(cursor: Cursor, record: T) -> T:
    cursor.execute(
        sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(record.get_schema(), record.get_tablename()),
            sql.SQL(", ").join(map(sql.Identifier, record.get_fieldnames())),
            sql.SQL(", ").join(
                sql.Placeholder() * len(record.get_fieldnames())
            ),
        ),
        [*record.get_values()],
    )
    return record


def create_many(cursor: Cursor, records: list[T]) -> list[T]:
    if len(records) == 0:
        return []
    schema = records[0].get_schema()
    tablename = records[0].get_tablename()
    record_type = type(records[0])
    fieldnames = records[0].get_fieldnames()
    with cursor.copy(
        sql.SQL("COPY {} ({}) FROM STDOUT").format(
            sql.Identifier(schema, tablename),
            sql.SQL(", ").join(map(sql.Identifier, fieldnames)),
        )
    ) as copy:
        for record in records:
            if not isinstance(record, record_type):
                raise ValueError(
                    "not the same record type"
                    f": f{record_type} and f{type(record)}"
                )
            copy.write_row(tuple(record.get_values()))
    return records

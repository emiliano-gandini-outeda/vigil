from dbwarden import database_config
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings

clickhouse = database_config(
    database_name="clickhouse",
    database_type="clickhouse",
    database_url_sync=settings.clickhouse_native_url,
    database_url_async=settings.clickhouse_async_url,
    default=True,
)

class Base(DeclarativeBase):
    pass
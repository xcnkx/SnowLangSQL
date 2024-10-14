from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection, Engine


class SnowflakeRepository:
    def __init__(
        self,
        account: str,
        user: str,
        warehouse: str,
        database: str,
        schema: str,
        authenticator: str = "externalbrowser",
    ) -> None:
        self.engine = create_engine(
            URL(
                account=account,
                user=user,
                warehouse=warehouse,
                database=database,
                schema=schema,
                authenticator=authenticator,
            )
        )

    def get_engine(self) -> Engine:
        return self.engine

    def get_connection(self) -> Connection:
        return self.engine.connect()

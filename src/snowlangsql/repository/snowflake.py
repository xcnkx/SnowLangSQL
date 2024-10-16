from langchain_community.utilities import SQLDatabase
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
        password: str | None = None,
    ) -> None:
        if password is not None:
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
        else:
            self.engine = create_engine(
                URL(
                    account=account,
                    user=user,
                    warehouse=warehouse,
                    database=database,
                    schema=schema,
                    password=password,
                )
            )

    def get_engine(self) -> Engine:
        return self.engine

    def get_connection(self) -> Connection:
        return self.engine.connect()

    def get_sqldatabase(self) -> SQLDatabase:
        return SQLDatabase(self.engine, view_support=True)

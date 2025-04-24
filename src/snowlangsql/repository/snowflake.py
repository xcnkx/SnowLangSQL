import os
from langchain_community.utilities import SQLDatabase
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Connection, Engine
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class SnowflakeRepository:
    def __init__(
        self,
        account: str,
        user: str,
        warehouse: str,
        database: str,
        schema: str,
        role: str | None = None,
        private_key_path: str | None = None,
        private_key_passphrase: str | None = None,
        authenticator: str = "externalbrowser",
    ) -> None:
        url_kwargs = {
            "account": account,
            "user": user,
            "warehouse": warehouse,
            "database": database,
        }
        if schema:
            url_kwargs["schema"] = schema
        if role:
            url_kwargs["role"] = role

        if private_key_path:
            # Key-Pair認証
            # 秘密鍵を読み込み
            with open(private_key_path, "rb") as key:
                p_key = serialization.load_pem_private_key(
                    key.read(),
                    password=private_key_passphrase.encode() if private_key_passphrase else None,
                    backend=default_backend()
                )

            # 秘密鍵をDER形式に変換
            pkb = p_key.private_bytes(
                encoding=serialization.Encoding.DER,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            )

            # Snowflakeエンジンを作成（Key-Pair認証）
            self.engine = create_engine(
                URL(**url_kwargs),
                connect_args={"private_key": pkb},
            )
        else:
            # SSO認証（externalbrowser）
            url_kwargs_auth = url_kwargs.copy()
            url_kwargs_auth["authenticator"] = authenticator
            self.engine = create_engine(
                URL(**url_kwargs_auth)
            )

    def get_engine(self) -> Engine:
        return self.engine

    def get_connection(self) -> Connection:
        return self.engine.connect()

    def get_sqldatabase(self) -> SQLDatabase:
        return SQLDatabase(self.engine, view_support=True)

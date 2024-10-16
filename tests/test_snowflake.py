import pytest
from sqlalchemy import text
from sqlalchemy.engine.base import Engine
from sqlalchemy.exc import SQLAlchemyError

from snowlangsql import config
from snowlangsql.repository.snowflake import SnowflakeRepository


@pytest.fixture(scope="module")
def snowflake_repository():
    # Snowflakeへの接続情報を設定
    account = config.SNOWFLAKE_ACCOUNT
    user = config.SNOWFLAKE_USER
    warehouse = config.SNOWFLAKE_WAREHOUSE
    database = config.SNOWFLAKE_DATABASE
    schema = config.SNOWFLAKE_SCHEMA
    password = config.SNOWFLAKE_PASSWORD

    return SnowflakeRepository(
        account=account, user=user, warehouse=warehouse, database=database, schema=schema, password=password
    )


def test_get_engine(snowflake_repository):
    engine = snowflake_repository.get_engine()

    assert isinstance(engine, Engine), "Engineのインスタンスではありません"

    try:
        # 実際にデータベースに接続してテスト
        with engine.connect() as connection:
            # text()を使って実行可能なSQLにする
            result = connection.execute(text("SELECT CURRENT_VERSION()"))
            version = result.fetchone()[0]
            print(f"Snowflake version: {version}")
            assert version is not None, "Snowflakeのバージョンが取得できませんでした"
    except SQLAlchemyError as e:
        pytest.fail(f"データベース接続に失敗しました: {e}")


def test_get_connection(snowflake_repository):
    try:
        with snowflake_repository.get_connection() as connection:
            # text()を使って実行可能なSQLにする
            result = connection.execute(text("SELECT CURRENT_USER(), CURRENT_ROLE()"))
            user, role = result.fetchone()
            print(f"Current user: {user}, Current role: {role}")

            assert user is not None, "ユーザー情報が取得できませんでした"
            assert role is not None, "ロール情報が取得できませんでした"
    except SQLAlchemyError as e:
        pytest.fail(f"クエリの実行に失敗しました: {e}")


def test_get_sqldatabase(snowflake_repository):
    sqldatabase = snowflake_repository.get_sqldatabase()

    assert sqldatabase is not None, "SQLDatabaseのインスタンスが取得できません"

    try:
        # 実際にデータベースに接続してテスト
        result = sqldatabase.get_usable_table_names()
        print(f"Usable table names: {result}")
        assert len(result) > 0, "テーブル名が取得できませんでした"
    except SQLAlchemyError as e:
        pytest.fail(f"テーブル名の取得に失敗しました: {e}")

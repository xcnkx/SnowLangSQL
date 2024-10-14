from snowlangsql.tools import list_tables_tool


def test_list_tables_tool():
    table_list = list_tables_tool.invoke("")

    assert table_list is not None

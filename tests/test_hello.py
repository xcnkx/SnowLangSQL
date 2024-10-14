from snowlangsql import hello


def test_hello():
    assert hello.main() == "Hello from snowlangsql!"

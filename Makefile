UV := uv
PYTEST := $(UV) run pytest
RUFF   := $(UV) run ruff
MYPY   := $(UV) run mypy

install:
	$(UV) sync

install-no-dev:
	$(UV) sync --no-dev

lint:
	$(RUFF) check src tests

type-check:
	$(MYPY) src

fix:
	$(RUFF) check src tests --fix
	$(RUFF) format src tests

test:
	$(PYTEST) -vv ./tests/$(TEST_TARGET)

run:
	$(UV) run streamlit run app.py
.PHONY: install lint types test all clean

isort = isort plate tests
black = black plate tests
mypy = mypy --install-types --non-interactive plate

install:
	@echo "Install editable package"
	pip install -r requirements.txt

lint:
	@echo "Run linters & formatters"
	$(isort)
	$(black)

types:
	@echo "Check type hints"
	$(mypy)

test:
	@echo "Run tests with coverage"
	pytest -vvs --cov=plate -cov_report=term-missing tests

all: install lint types test

clean:
	@echo "Clean up files"
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -rf .cache
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf htmlcov
	rm -rf *.egg-info
	rm -f .coverage
	rm -f .coverage.*
	rm -rf build
	rm -rf dist

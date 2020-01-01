.PHONY: clean lint test coverage

clean:
	rm -r */__pycache__/
	rm -r .pytest_cache/
	rm .coverage

coverage:
	pytest -s --cov=mbta tests/ --cov-report xml:cov.xml

lint:
	flake8 --ignore=E221,E501 mbta tests

test:
	pytest -s --cov=mbta tests/

.PHONY: clean lint test coverage

clean:
	rm -r */__pycache__/
	rm -r .pytest_cache/
	rm .coverage

coverage:
	pytest --cov=mbta tests/

lint:
	flake8 --ignore=E221,E501 mbta tests

test:
	pytest tests/

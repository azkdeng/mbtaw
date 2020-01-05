.PHONY: clean lint test coverage

clean:
	rm -r */__pycache__/
	rm -r .pytest_cache/
	rm .coverage

coverage:
	pytest -s --cov=mbtaw tests/ --cov-report xml:cov.xml

lint:
	flake8 --ignore=E221,E501 mbtaw tests

test:
	pytest -s --cov=mbtaw tests/

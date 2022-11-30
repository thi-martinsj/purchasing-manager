clean:
	@echo "Clean - Removing the following files/directories (*.pyc, *.pyo, *.pytest_cache, .coverage, htmlcov, test_reports)"
	@find . -name "*.pyc" -delete && \
	find . -name "*.pyo" -delete && \
	find . -name .pytest_cache | xargs rm -rf || true && \
	find . -name __pycache__ -delete && \
	rm -f src/.coverage && \
	rm -rf src/htmlcov && \
	rm -rf src/test_reports

isort-fix:
	@echo "Isort Fix- Organizing all import statements"
	@isort --settings-path=pyproject.toml src/.

black-fix:
	@echo "Black Fix - Running code formatter"
	@black src/.

lint:
	@echo "Lint - Running lint"
	@flake8 --config=.flake8 src/*

tests: clean lint 
	@echo "Tests - Running testing without coverage"
	@cd src && pytest tests/ -s -v

coverage: clean lint
	@echo "Coverage - Running testing with coverage"
	@cd src && pytest --cov-report term-missing --cov=purchasing_manager -s -vv \
	--junitxml=test_reports/junit.xml --cov-branch --cov-report=term --cov-report=html

run: clean
	@cd src && flask run -p 5000
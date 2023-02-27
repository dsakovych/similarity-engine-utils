venv:
	test ! -d venv && python3.10 -m virtualenv venv; \
	. venv/bin/activate; \
	python3.10 install -U pip; \
	python3.10 -m pip install -r requirements.txt; \

clean:
	rm -rf `find . -name __pycache__`
	rm -f `find . -type f -name '*.py[co]' `
	rm -f `find . -type f -name '*~' `
	rm -f `find . -type f -name '.*~' `
	rm -f `find . -type f -name '@*' `
	rm -f `find . -type f -name '#*#' `
	rm -f `find . -type f -name '*.orig' `
	rm -f `find . -type f -name '*.rej' `
	rm -f `find . -type f -name '*.egg-info' `
	rm -rf `find ./  -name '*.egg-info'`
	rm -f .coverage
	rm -rf coverage
	rm -rf cover
	rm -rf htmlcov
	rm -rf .cache
	rm -rf .eggs
	rm -rf *.egg-info
	rm -rf .env
	rm -rf .pytest_cache
	rm -rf dist

doc:
	make -C docs clean html

lint:
	PYTHONPATH=`pwd` pylint --rcfile=pylint.conf src

lint_fix:
	flake8 src; \
	isort src

unittest:
	PYTHONPATH=`pwd` python -m pytest tests -v

coverage:
	PYTHONPATH=`pwd` coverage run -m pytest tests -v; coverage report -m

build:
	python -m build; \
	twine check dist/*;

upload:
	twine upload --verbose dist/*

.PHONY: lint
lint:
	isort watcher tests
	black watcher tests
	flake8 watcher tests
	mypy --ignore-missing-imports watcher tests

.PHONY: check
check:
	isort --check watcher tests
	black --check watcher tests
	flake8 watcher tests
	mypy --ignore-missing-imports watcher tests
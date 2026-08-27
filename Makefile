.PHONY: help run lint docker-build docker-run compose test clean security

help:
	@echo "Available targets:"
	@echo "  run          - Run locally"
	@echo "  lint         - Run flake8"
	@echo "  docker-build - Build Docker image"
	@echo "  docker-run   - Build and run Docker container"
	@echo "  compose-up   - Run with docker composer"
	@echo "  compose-down - Down with docker composer"
	@echo "  test         - Run pytest"
	@echo "  clean        - Remove Python cache"
	@echo "  security     - make security checks"

run:
	python3 server.py

lint:
	@which flake8 > /dev/null || (echo "flake8 not installed, run: pip install flake8" && exit 1)
	flake8 server.py

docker-build:
	docker build -t my-encoder .

docker-run: docker-build
	docker run -d -p 8080:8080 my-encoder

compose-up:
	docker-compose up -d

compose-down:
	docker-compose down

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -name "*.pyc" -delete

security:
	bandit -r . -x tests
	pip-audit
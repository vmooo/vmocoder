# vmocoder

A lightweight Python HTTP microservice that converts text between different encodings and formats.

## DevOps Toolchain

1. **Dockerfile** – multi‑stage (or simple) container image with Python 3.11, running as non‑root user.
2. **Docker Compose** – one‑command local development setup with environment variables.
3. **Makefile** – common tasks aliased: `make run`, `make test`, `make lint`, `make docker‑build`, etc.
4. **CI/CD with GitHub Actions** – automated pipeline that runs:
   - Linting (`flake8`)
   - Unit tests (`pytest`)
   - Security scanning (`bandit` and `trivy`)
   - Docker image build (always)
   - **Continuous Delivery** – on every push to `main`, the image is built and pushed to **GitHub Container Registry (GHCR)** with `:latest` and commit‑SHA tags.

## Security

- Static analysis – bandit is used to scan Python code for common vulnerabilities (excluded tests/).
- Container scanning – trivy checks the final Docker image for known CVEs in OS packages and Python dependencies.
- Secrets – all sensitive data (GHCR token, SSH keys) are stored as GitHub Secrets, never hardcoded.

## Getting Started on Linux/MacOS

### Prerequisites

- Python 3.11+
- Docker (optional)
- Docker Compose (optional)

### Getting ready Docker image

You can get the latest Docker image from ghcr:
```bash
docker pull ghcr.io/vmooo/vmocoder:latest 
```

And run it
```bash
docker run -d -p 8080:8080 vmocoder
```

### Run locally

```bash
python3 server.py
```

### Run with Docker

```bash
docker build -t vmocoder .
```

```bash
docker run -d --rm -p 8080:8080 --name app vmocoder
```

### Run with Docker Compose

```bash
docker-compose up
```

### Run with `Makefile`

```bash
make docker-run
```

or 

```bash
make compose-up
```

### Possible problems

If the page doesn't load сheck if the port on the host is busy:
```bash
sudo lsof -i :8080
```
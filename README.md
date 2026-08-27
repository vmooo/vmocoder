# vmocoder


## How to run an application on Linux/MacOS

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
docker-compose up -d
```

### Possible problems

If the page doesn't load сheck if the port on the host is busy:
```bash
sudo lsof -i :8080
```
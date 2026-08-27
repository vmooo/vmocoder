# vmocoder

## How to run an application on Linux/MacOS

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
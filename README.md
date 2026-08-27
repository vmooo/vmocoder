# vmocoder

## Run locally

```bash
python3 server.py
```

## Run with Docker

```bash
docker build -t vmocoder .
```

```bash
docker run -d --rm -p 8080:8080 --name app vmocoder
```

## Possible problems

If the page doesn't load сheck if the port on the host is busy
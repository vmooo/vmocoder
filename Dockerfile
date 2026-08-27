FROM python:3.11-slim

WORKDIR /app

COPY server.py index.html ./

RUN addgroup --system app && adduser --system --group app
USER app

EXPOSE 8080

CMD ["python3", "server.py"]
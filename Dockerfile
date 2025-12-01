# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.13-slim AS builder

WORKDIR /app

RUN apt-get update

#RUN apt-get install -y pkg-config python3-dev default-libmysqlclient-dev build-essential
RUN apt-get install -y libmysqlclient-dev


# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Set the polygon.io API key
ENV POLYGON_API_KEY=###

# Set the Tiingo API key
ENV TIINGO_API_KEY=###

# Set the Tiingo API key
ENV COMWYCA_API_KEY=###

# Set the mongodb host
ENV MONGODB_HOST=mongo

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Create a volume
VOLUME /data/market_analysis

FROM python:3.13-slim

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . /usr/src/app
WORKDIR /usr/src/app

# run docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["./manage.py", "runserver", "0.0.0.0:8001"]
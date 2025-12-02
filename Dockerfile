FROM python:3.13 AS builder

WORKDIR /app

# General Packages
RUN apt-get update \
    && apt-get install -y python3-dev \
    && apt-get install -y default-libmysqlclient-dev \
    && apt-get install -y build-essential \
    && apt-get install -y pkg-config \
    && pip install --upgrade pip

# venv 
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Create a volume
VOLUME /data/export

FROM python:3.13

WORKDIR /app

COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# venv
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip
RUN pip install --no-cache /wheels/*

COPY . /usr/src/app
WORKDIR /usr/src/app

# run docker-entrypoint.sh
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]

CMD ["./manage.py", "runserver", "0.0.0.0:8001"]
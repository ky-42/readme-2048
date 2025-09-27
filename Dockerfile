FROM python:3.11-slim AS builder

WORKDIR /app

# install build dependencies required for building wheels (and Poetry)
RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock README.md ./
COPY src ./src

# Build wheel into ./dist
RUN poetry build -f wheel -o ./dist

FROM python:3.11-slim

WORKDIR /app

# Copy the wheel built in the previous stage
COPY --from=builder /app/dist/*.whl ./dist/

# Install gunicorn and the application wheel
RUN pip install --no-cache-dir gunicorn ./dist/*.whl

RUN apt-get update && apt-get install -y git openssh-client

# Expose port (optional, helpful for documentation)
EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "src:app"]
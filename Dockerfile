FROM python:3.13.3-alpine3.21

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
ADD . /mcp

# Sync the project into a new environment, asserting the lockfile is up to date
WORKDIR /mcp
RUN apk add --no-cache gcc python3-dev musl-dev linux-headers
RUN uv sync --locked  --no-dev

EXPOSE 10000

CMD ["sh", "-c", "uv run authentication/generate_key.py && uv run src/server.py --host 0.0.0.0 --port 10000"]
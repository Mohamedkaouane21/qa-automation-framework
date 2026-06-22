# Reproducible test runner. The official Playwright image already ships the
# browsers and their system dependencies, so the suite runs identically on a
# laptop and in CI.
FROM mcr.microsoft.com/playwright/python:v1.60.0-noble

WORKDIR /app

# Install Python dependencies first for better layer caching.
COPY pyproject.toml ./
COPY src ./src
RUN pip install --no-cache-dir -e ".[dev]"

# Copy the rest of the project.
COPY . .

# Default: run the whole suite (override CMD to target a marker, e.g.
#   docker run --rm qa-framework pytest -m api).
CMD ["pytest", "-m", "unit or api"]

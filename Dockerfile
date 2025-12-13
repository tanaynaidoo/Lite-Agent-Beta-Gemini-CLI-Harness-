# Stage 1: Build dependencies
FROM python:3.12-slim-bookworm AS builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    # Add any other system dependencies needed for your Python packages
    # Example: libpq-dev for psycopg2, if you use PostgreSQL
    # libgl1-mesa-glx for some UI/graphical libraries, if needed
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Final application image
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy source code
COPY . .

# Ensure the agent runs as a non-root user (good security practice)
# Adjust user/group as needed, or create a specific one
# RUN useradd --no-create-home appuser
# USER appuser

# Define the command to run your agent
# This will depend on your agent's entry point
# For now, let's assume it's a Python script in src/
# CMD ["python", "src/your_agent_entrypoint.py"]
# Or if it's a CLI:
# ENTRYPOINT ["python", "-m", "src.your_module"]
# CMD ["help"]

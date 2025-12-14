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

# Copy pyproject.toml and requirements.txt to leverage Docker cache
COPY pyproject.toml .
COPY requirements.txt .

# Create virtual environment and install build-time dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# Install project in editable mode to make 'esl-harness' command available
# Also installs dependencies from pyproject.toml and requirements.txt
RUN pip install --no-cache-dir -e .


# Stage 2: Final application image
FROM python:3.12-slim-bookworm

WORKDIR /app

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy essential application files
# This is a more targeted copy than 'COPY . .'
# Assuming 'src' is where the main application logic resides
COPY src ./src
COPY pyproject.toml .
COPY HARNESS_CONTRACT.md .
# Important for documentation and contract
COPY README.md .
# For quick reference inside container

# Copy host adapters (if they are needed inside the container for some reason, e.g., for local testing of adapters)
COPY host ./host


# Ensure the agent runs as a non-root user (good security practice)
# Adjust user/group as needed, or create a specific one
# RUN useradd --no-create-home appuser
# USER appuser

# Define the command to run your agent, using the 'esl-harness' CLI
ENTRYPOINT ["esl-harness"]
CMD ["--help"] # Default command to show help if no other command is provided

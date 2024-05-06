# Dockerfile
FROM python:3.12-slim-bookworm

# Set environment variables
ENV APP_HOME /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR $APP_HOME

# Install system dependencies
RUN apt update -y
RUN apt install curl -y

# Install torch (CPU version)
# https://pytorch.org/get-started/locally/
# RUN pip install torch==2.2.0+cpu torchvision==0.17.0+cpu torchaudio==2.2.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-deps sentence-transformers

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at $APP_HOME
COPY . $APP_HOME

# Expose the port the app runs on
EXPOSE 5681

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 9876 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

HEALTHCHECK --interval=60s --timeout=5s --retries=5\
    CMD curl -f http://localhost:5681/healthcheck || exit 1
FROM python:3.10-slim

### ENVIRONMENT VARIABLES ###
ENV PYTHONUNBUFFERED=1
ENV WATCHFILES_FORCE_POLLING=true

# Set the working directory in the container
WORKDIR /api

# Copy only requirements.txt first to leverage Docker cache for dependency installation
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Run the application with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port 3000 --reload
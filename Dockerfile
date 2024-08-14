# Use a Python 3.9 full version image to build and install mysqlclient
FROM python:3.9 AS python-build
RUN pip install mysqlclient

# Use a slim Python 3.9 image for the final stage
FROM python:3.9-slim

# Install necessary system libraries
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    libmariadb-dev-compat \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy installed packages from the build stage
COPY --from=python-build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy the requirements file to the container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code to the container
COPY . .

# Specify the port on which your application will run
EXPOSE 8000

# Upgrade pip
RUN pip install --upgrade pip

# Run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ktscrm.wsgi:application"]

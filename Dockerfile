# Use a Python 3.9 full version image to build and install mysqlclient
FROM python:3.9 AS python-build
RUN pip install mysqlclient

# Use a slim Python 3.9 image for the final stage
FROM python:3.9-slim-buster

# Install necessary system libraries and tools
RUN apt-get update && apt-get install -y \
    curl \
    gnupg2 \
    unixodbc \
    unixodbc-dev \
    libpq-dev \
    gcc \
    libmariadb-dev-compat \
    pkg-config \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Add the Microsoft package signing key and repository for Debian Buster
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add - \
    && curl https://packages.microsoft.com/config/debian/10/prod.list | tee /etc/apt/sources.list.d/mssql-release.list \
    && apt-get update

# Install the ODBC driver for SQL Server
RUN ACCEPT_EULA=Y apt-get install -y msodbcsql17

# Clean up APT when done.
RUN apt-get clean -y \
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

RUN python manage.py collectstatic --noinput

# Run your application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "ktscrm.wsgi:application"]

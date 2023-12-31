FROM python:3.12-bookworm

# Select working directory
WORKDIR /code

# Copy requirements.txt to working directory
COPY requirements.txt requirements.txt


# Install dependencies
RUN pip install -r requirements.txt

# Copy source code to working directory
COPY . /code

# Create data directory
RUN mkdir -p /data/logs

# Run the application
CMD ["python3", "main.py"]

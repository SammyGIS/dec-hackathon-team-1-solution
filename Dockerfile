# Use Python 3.9 as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt ./requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the application code and environment variables
COPY etl_script.py ./etl_script.py
COPY .env ./


# Run the application
CMD ["python", "etl_script.py"]

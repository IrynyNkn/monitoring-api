FROM python:3.11.8-slim

# Set the working directory in the container
WORKDIR /source

COPY ./requirements.txt /source
COPY ./alembic.ini /source

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY ./app /source/app

# Command to run the uvicorn server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
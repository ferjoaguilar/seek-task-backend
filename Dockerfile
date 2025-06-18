# Use the official Python image from the Docker Hub
FROM python:3.12

# Set the working directory in the container
WORKDIR /code

# Install wkhtmltopdf
RUN apt-get update && apt-get install -y wkhtmltopdf

# Copy the requirements file into the container
COPY ./requirements.txt /code/requirements.txt

# Install the dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy the rest of the application code into the container
COPY ./app /code/app

# Expose the port the app runs on
EXPOSE 80

# Command to run the FastAPI application with command fastapi run app/main.py
CMD ["fastapi", "run", "app/main.py", "--port", "80"]
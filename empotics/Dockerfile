# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY req.txt .

# Install project dependencies
RUN pip install --no-cache-dir -r req.txt

# Copy the Django project code to the working directory
COPY . .

# Expose the port your Django app will run on
EXPOSE 8000

# Define the command to run when the container starts
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

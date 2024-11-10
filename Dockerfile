# Use the official Python image as a base
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code into the container
COPY . .

# Expose port 8000 for the application
EXPOSE 8000

# Command to run your application
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
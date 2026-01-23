# Dockerfile

# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED 1

# *** CRITICAL CHANGE 1: Set the working directory to the backend subdirectory ***
WORKDIR /srv/contribs/backend

# Install dependencies (requirements.txt must be in the same context as this Dockerfile)
# Assuming requirements.txt is at the project root (where docker-compose.yml is)
# We need to copy it into the correct path inside the container:
COPY requirements.txt /srv/contribs/backend/

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code. This copies everything from the root
# of your local project (which includes the 'backend' folder) into the WORKDIR
# defined above, which is /srv/contribs/backend.
COPY . /srv/contribs/backend/

# Expose the port Django runs on
EXPOSE 8000

# Command to run the Django server
# The 'manage.py' file will now be found directly in the WORKDIR
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

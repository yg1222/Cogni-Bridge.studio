# Base image for the build stage
FROM python:3.11-bullseye AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y build-essential

# Copy the source code into the container
COPY . /app

# Set the working directory for subsequent commands
WORKDIR /app

# Install dependencies required for building the application
RUN pip install --upgrade pip 

# Explicitly setting path for flask
ENV PATH="/app/bin:${PATH}"

RUN pip list
RUN pwd
RUN ls

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

RUN echo "CONFIRMATION VIEW" && ls -all

# Run app
#CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "--port=5000"]
# CMD ["flask", "run", "--host=0.0.0.0"]
# CMD ["gunicorn", "wsgi", ":","app"]
CMD ["gunicorn", "-w", "4", "wsgi:app"]
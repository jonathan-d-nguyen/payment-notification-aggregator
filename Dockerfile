# Use an official Python runtime as a parent image
# FROM python:3.9-slim
FROM python:alpine3.19

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --upgrade google-api-python-client
RUN pip install --upgrade google-auth google-auth-oauthlib google-auth-httplib2
RUN pip install --upgrade flask
RUN pip install --upgrade requests

# Define environment variable (if needed)
ENV NAME World

# Run app.py when the container launches
CMD ["python", "gmail-credential.py"]
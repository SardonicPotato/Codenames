 # Use an official Python runtime as a base image
FROM python:3.6-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
ADD . /app

# Need gcc to install gensim
RUN apt-get update && apt-get install -y gcc wget

# Install any needed packages specified in requirements.txt
RUN pip install -r requirements.txt

RUN python setup.py install

RUN python scripts/generate_model_data.py ./data

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "webserver/server.py", "./data"]

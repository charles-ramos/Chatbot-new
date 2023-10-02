# Use an official Python runtime as a parent image
FROM python:3.6.10

# Set the working directory in the container to /app
WORKDIR /chatbot

# Add the current directory contents into the container at /app
ADD . /chatbot

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8081 available to the world outside this container
EXPOSE 8200

# Run app.py when the container launches
CMD ["python", "chatbot.py"]

docker build -t docker_flask:latest .
docker run my-service -p 8200:8200 --network="host"

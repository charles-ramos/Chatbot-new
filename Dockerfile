```
# Use an official updated Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /chatbot

# Add the current directory contents into the container at /app
ADD . /chatbot

# Install build dependencies
RUN apt-get update && apt-get install -y gcc python3-dev

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["python", "routes.py"]

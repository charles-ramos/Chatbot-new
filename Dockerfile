# Use an official updated Python runtime as a parent image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /chatbot

# Copy the current directory contents into the container at /app
COPY . /chatbot

# Update package list
RUN apt-get update

# Install build dependencies
RUN apt-get install -y gcc python3-dev libatlas-base-dev

# Update pip
RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80/tcp

# Run app.py when the container launches
CMD ["python", "routes.py"]

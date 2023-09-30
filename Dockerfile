FROM debian:latest

# Set the working directory in the container to /app
WORKDIR /chatbot

# Copy the current directory contents into the container at /app
COPY . /chatbot

# Update package list
RUN apt-get update

# Install build dependencies
RUN apt-get install -y gcc python3-dev libatlas-base-dev python3-pip python3-venv pipx

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80/tcp

# Run app.py when the container launches
CMD ["executable","param1","param2"]

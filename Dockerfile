# Use an official Python runtime as a parent image
FROM python:3.6.10

# Set the working directory in the container to /app
WORKDIR /chatbot

COPY requirements.txt /chatbot

# Add the current directory contents into the container at /app
COPY . /chatbot

RUN /usr/local/bin/python -m pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r /chatbot/requirements.txt

# Make port 8081 available to the world outside this container
EXPOSE 8081

# Run app.py when the container launches
#CMD ["python", "/chatbot/chatbot.py"]
CMD ["gunicorn", "-b", "0.0.0.0:8081", "app:chatbot"]


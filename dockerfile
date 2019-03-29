# Use an official Python runtime as a parent image
FROM python:3.7.0

# Set the working directory
WORKDIR /TexasHoldemBot

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME SlackTexasHoldemBot

# Run app.py when the container launches
CMD ["python3", "runBot.py"]
# Use an official Ubuntu as a parent image
FROM ubuntu:20.04

# Set environment variables to prevent interactive prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install Python and system dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip alsa-utils && \
    apt-get clean

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Python dependencies specified in requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container (optional)
EXPOSE 80

# Run the application
CMD ["python3", "daq_pi.py"]

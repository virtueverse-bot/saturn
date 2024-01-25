# Use an official Python runtime as a parent image
FROM python:3.9.6

# Install system dependencies (including ImageMagick)
RUN apt-get update && apt-get install -y \
    imagemagick

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 5000 available to the world outside this container
EXPOSE 5000



# Run app.py when the container launches
CMD ["python3", "start.py"]

FROM node:20

# Set the working directory in the container
WORKDIR /app

# Install Node.js dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install

# Copy the requirements file
COPY requirements.txt .

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -r requirements.txt
# Install Python and required libraries
# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Command to run the application
CMD ["node", "index.js"]
# Use the official Python base image

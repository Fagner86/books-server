FROM node:20

# Set the working directory in the container
WORKDIR /app

# Install Node.js dependencies
COPY package.json .
COPY package-lock.json .
RUN npm install

# Install Python and required libraries
RUN apt-get update && apt-get install -y python3 python3-pip

# Install scikit-learn using pip
RUN pip3 install --no-cache-dir scikit-learn

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Command to run the application
CMD ["node", "index.js"]
# Use the official Python base image

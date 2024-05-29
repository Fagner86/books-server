# Use the official Node.js image as a base
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files
COPY package.json .
COPY package-lock.json .

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 8080

# Install Python and required libraries
RUN apt-get update && apt-get install -y python3 python3-pip

# Install scikit-learn using pip in a virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install scikit-learn

# Command to run the application
CMD ["node", "index.js"]

FROM node:20

# Set the working directory in the container
WORKDIR /app

# Install Python and required libraries
RUN apt-get update && apt-get install -y python3 python3-pip python3-dev build-essential

# Install additional dependencies required for scikit-learn
RUN apt-get install -y libatlas-base-dev gfortran

# Install scikit-learn
RUN pip3 install --no-cache-dir scikit-learn

# Copy the package.json and package-lock.json files
COPY package.json .
COPY package-lock.json .

# Install Node.js dependencies
RUN npm install

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Command to run the application
CMD ["node", "index.js"]

# Use an official Node.js runtime as a parent image
FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json .
COPY package-lock.json .

# Install Node.js dependencies
RUN npm install

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# Install Python dependencies
RUN pip install scikit-learn

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on
EXPOSE 4000

# Define the command to run the app
CMD ["node", "index.js"]

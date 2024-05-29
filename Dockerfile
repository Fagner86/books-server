# Use the official Node.js image as a base
FROM node:20

# Set the working directory in the container
WORKDIR /app

# Copy the package.json and package-lock.json files to the container
COPY package.json package-lock.json ./

# Install the dependencies
RUN npm install

# Copy the rest of the application code to the container
COPY . .

# Install Python and required libraries
RUN apt-get update && apt-get install -y python3 python3-pip
RUN pip3 install scikit-learn

# Expose the port the app runs on
EXPOSE 4000

CMD ["node", "index.js"]
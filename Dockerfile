# Use a base image that has Node.js and Python
FROM node:20

WORKDIR /app

COPY package.json .
COPY package-lock.json .

RUN npm install

# Copy the Node.js source code
COPY . .

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install scikit-learn
RUN apt-get update && apt-get install -y scikit-learn

# Expose the port that the application will run on
EXPOSE 4000

# Define environment variables
ENV PORT=4000

# Command to run the application
CMD ["node", "index.js"]

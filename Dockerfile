FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json .
COPY package-lock.json .

# Install node dependencies
RUN npm install

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Python dependencies
RUN pip install scikit-learn

# Copy the rest of the application code
COPY . .

# Run the application
CMD ["npm", "start"]

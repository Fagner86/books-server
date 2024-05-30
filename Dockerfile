FROM node:20

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package.json .
COPY package-lock.json .

# Install node dependencies
RUN npm install

# Install Python, pip, and venv
RUN apt-get update && apt-get install -y python3 python3-pip python3-venv

# Create a virtual environment
RUN python3 -m venv /app/venv

# Activate the virtual environment and install Python dependencies
RUN /app/venv/bin/pip install scikit-learn

# Copy the rest of the application code
COPY . .

# Ensure the virtual environment is activated and the application is started
CMD ["/bin/bash", "-c", "source /app/venv/bin/activate && node index.js"]

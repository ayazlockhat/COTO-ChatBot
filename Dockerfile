# Use an official Python image
FROM python:3.10

# Install Node.js and necessary utilities
RUN apt-get update && apt-get install -y nodejs npm

# Set the working directory inside the container
WORKDIR /app

# Copy only necessary files for dependency installation
COPY package.json package-lock.json /app/
COPY backend/requirements.txt /app/backend/

# Install backend dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Install frontend dependencies
RUN npm install

# Copy the rest of the project
COPY . /app/

# Build the frontend for production
RUN npm run build

# Expose necessary ports
EXPOSE 8000 8501

# Run backend and frontend properly
CMD ["bash", "-c", "python backend/scrape_articles.py && python backend/embed_articles.py && python backend/main.py & npx serve -s src/dist -l 8501"]

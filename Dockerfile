# Use an official Python image
FROM python:3.10

# Install Node.js and necessary utilities
RUN apt-get update && apt-get install -y nodejs npm

# Set the working directory inside the container
WORKDIR /app

# Copy everything from the root directory
COPY . /app/

# Install backend dependencies
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Set the working directory for frontend before installing dependencies
WORKDIR /app

# Install frontend dependencies
RUN npm install

# Build the frontend for production
RUN npm run build

# Expose necessary ports
EXPOSE 8000 8501

# Run backend and frontend properly
CMD ["bash", "-c", "python backend/scrape_articles.py && python backend/embed_articles.py && python backend/main.py & npx serve -s src/dist -l 8501"]

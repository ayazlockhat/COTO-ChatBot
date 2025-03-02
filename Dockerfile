# Use an official Python image
FROM python:3.10

# Install Node.js and necessary utilities
RUN apt-get update && apt-get install -y nodejs npm

# Set the working directory inside the container
WORKDIR /app

### ---- BACKEND SETUP ---- ###
# Copy only the backend dependencies first (for efficient caching)
COPY backend/requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the entire backend code
COPY backend /app/backend

### ---- FRONTEND SETUP ---- ###
# Copy frontend-related files (only what's needed)
COPY package.json package-lock.json vite.config.ts tsconfig.json tailwind.config.js postcss.config.js ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY src /app/src

# Build the frontend for production
RUN npm run build

# Expose necessary ports
EXPOSE 8000 8501

# Run backend and frontend properly
CMD bash -c "python backend/scrape_articles.py && python backend/embed_articles.py && python backend/main.py & npx serve -s src/dist -l 8501"

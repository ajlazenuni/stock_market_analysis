FROM node:18-alpine

WORKDIR /usr/src/app

# Copy package files
COPY package*.json ./

# Install dependencies with platform-specific flag
RUN npm install --platform=linux --arch=x64 

# Copy project files
COPY . .

# Add this line to fix the rollup issue
RUN npm install @rollup/rollup-linux-x64-musl

EXPOSE 5173

# Update command
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
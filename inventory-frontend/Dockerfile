# Use an official Node.js image as the base
FROM node:18-alpine AS builder

# Set working directory inside the container
WORKDIR /ecommerce-microservices-app/inventory-frontend

# Copy package.json and package-lock.json first (to optimize caching)
COPY package.json package-lock.json ./

# Install dependencies
RUN npm install

# Copy the rest of the app files
COPY . .

# Build the React app
RUN npm run build

# Use Nginx to serve the built files
FROM nginx:stable-alpine

# Copy built React files to Nginx's serving directory
COPY --from=builder /ecommerce-microservices-app/inventory-frontend/build /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]

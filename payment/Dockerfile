# Use an official Python from Docker Hub as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /ecommerce-microservices-app/payment

# Copy the current directory contents into the container
COPY . .

# Install dependencies from requirement.txt
RUN pip install --no-cache-dir -r requirements.txt

# Give execution permissions to the startup script.
RUN chmod +x start.sh

# Expose port for FastAPI
EXPOSE 8001

# Run the startup script
CMD ["sh", "./start.sh"]
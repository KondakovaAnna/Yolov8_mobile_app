FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the bentofile.yaml and install dependencies
COPY bentofile.yaml .
RUN pip install bentoml

# Copy the rest of your application code
COPY . .

# Command to run your BentoML service
CMD ["bentoml", "serve", "yolo_v8:3dygx2nvuof56ogv"]
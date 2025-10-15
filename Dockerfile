# 1. Use an official Python runtime as a parent image
FROM python:3.9-slim

# 2. Set the working directory inside the container
WORKDIR /app

# 3. Copy the file with our dependencies
COPY requirements.txt .

# 4. Install the dependencies
# --no-cache-dir makes the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy our application code into the container
COPY app.py .

# 6. Tell Docker that our app runs on port 5000
EXPOSE 5000

# 7. Define the command to run when the container starts
CMD ["python", "app.py"]
# official Python image 
FROM python:3.9-slim

# Setting the working directory 
WORKDIR /usr/src/app

# Copying the requirements 
COPY requirements.txt ./

# Installing the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Creating an output directory
RUN mkdir /usr/src/app/output

# Copying the rest of the application code into the container
COPY . .

# runing the script
CMD ["python", "./sales_trends.py"]

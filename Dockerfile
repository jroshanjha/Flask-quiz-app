FROM python:3.11-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD python -u app.py



# FROM nginx:alpine

# # Set the working directory
# WORKDIR /usr/share/nginx/html

# # Copy dashboard files to Nginx html directory
# COPY . /usr/share/nginx/html

# # Expose port 80
# EXPOSE 80

# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]

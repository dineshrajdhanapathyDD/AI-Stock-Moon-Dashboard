FROM python:3.9-slim

WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Build static dashboard
RUN python build_static_dashboard.py

# Use nginx to serve static files
FROM nginx:alpine
COPY --from=0 /app/index.html /usr/share/nginx/html/
COPY --from=0 /app/data.json /usr/share/nginx/html/

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
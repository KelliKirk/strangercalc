FROM python:3.11-slim
WORKDIR /app

# Kopeeri requirements.txt backend kaustast
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopeeri kõik vajalikud failid
COPY app.py .
COPY backend/ ./backend/

# Kopeeri static ja templates ainult kui on olemas
COPY static/ ./static/ 2>/dev/null || true
COPY templates/ ./templates/ 2>/dev/null || true

EXPOSE 8000
CMD ["python", "app.py"]
# Gebruik een officiële Python-image als basis
FROM python:3.11-slim

RUN apt-get update && apt-get install -y git && apt-get clean
# Zet werkdirectory in container
WORKDIR /app

# Kopieer vereiste bestanden
COPY requirements.txt .

# Installeer Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Kopieer de rest van de app
COPY . .

# Expose de poort waarop Streamlit draait
EXPOSE 8501

# Start Streamlit automatisch
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.enableCORS=false"]

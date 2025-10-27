# Base Image
FROM python:3.10-slim

# Working Directory
WORKDIR /app
COPY . .

# Install Dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose Streamlit and Anki Ports
EXPOSE 8501
EXPOSE 8765
    
# Default Command
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0"]
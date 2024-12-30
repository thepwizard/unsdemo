FROM python:3.9-slim

WORKDIR /app

COPY main.py .

RUN pip install pymongo pandas streamlit

CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]

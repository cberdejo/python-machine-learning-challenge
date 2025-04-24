FROM python:3.11-slim

WORKDIR /app


# Copiar el resto del código
COPY . .

RUN pip install --upgrade pip setuptools wheel
RUN pip install .


# Lanzar la app de Streamlit
CMD ["streamlit", "run", "src/visualization/app.py", "--server.port=8501", "--server.address=0.0.0.0"]

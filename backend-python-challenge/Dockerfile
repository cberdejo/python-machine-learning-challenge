FROM python:3.11-slim

WORKDIR /app

# Instalar herramientas básicas
RUN apt-get update && apt-get install -y build-essential

# Copiar el resto del código
COPY . .


RUN pip install --upgrade pip setuptools wheel
RUN pip install .


# Lanzar el backend con Uvicorn
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]


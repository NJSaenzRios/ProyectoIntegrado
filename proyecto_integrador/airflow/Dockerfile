# Usar la imagen base de Apache Airflow
FROM apache/airflow:2.10.5

# Establecer el directorio de trabajo
WORKDIR /opt/airflow

# Crear el usuario airflow si no existe
RUN useradd --create-home --shell /bin/bash airflow || true

# Cambiar al usuario root para instalar paquetes
USER root
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libssl-dev \
    libffi-dev \
    python3-dev \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Cambiar al usuario airflow
USER airflow

# Copiar y instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar los archivos del DAG
COPY src /opt/airflow/dags/src

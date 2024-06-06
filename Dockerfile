FROM apache/airflow:2.6.0-python3.9

USER root

# Install necessary packages
RUN apt-get update && apt-get install -y \
    netcat \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Install Python packages
COPY requirements.txt /requirements.txt
RUN pip install --user -r /requirements.txt

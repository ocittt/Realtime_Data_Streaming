#!/bin/bash

set -e

echo "Starting script execution..."

if [ -e "/opt/airflow/requirements.txt" ]; then
    echo "Installing Python packages from requirements.txt..."
    python -m pip install --upgrade pip
    pip install --user -r /opt/airflow/requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
    echo "Initializing Airflow database..."
    airflow db init
    echo "Creating Airflow user..."
    airflow users create \
        --username admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@example.com \
        --password admin
fi

echo "Upgrading Airflow database..."
airflow db upgrade

echo "Starting Airflow webserver and scheduler..."
exec airflow webserver & exec airflow scheduler

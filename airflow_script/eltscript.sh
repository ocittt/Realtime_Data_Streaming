#!/bin/bash

set -e
## Exit immediately if a command exits with a non-zero status

echo "Starting script execution..."
## the start of script execution

if [ -e "/opt/airflow/requirements.txt" ]; then
    ## Check if the requirements.txt file exists in the specified directory

    echo "Installing Python packages from requirements.txt..."
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    ## a message indicating the installation of Python packages
    ## Upgrade pip
    ## Install packages listed in requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
    ## Check if the Airflow database file does not exist

    echo "Initializing Airflow database..."
    ## the initialization of the Airflow database started

    airflow db init
    echo "Creating Airflow user..."
    ## Initialize the Airflow database
    ##  a message indicating the creation of an Airflow user

    airflow users create \
        --username admin \
        --firstname admin \
        --lastname admin \
        --role Admin \
        --email admin@example.com \
        --password admin
    ## Create an admin user for Airflow with the specified credentials
fi

echo "Upgrading Airflow database..."
airflow db upgrade
## a message upgrade of the Airflow database
## Upgrade the Airflow database

echo "Starting Airflow webserver and scheduler..."
exec airflow webserver
## a message the start of the Airflow webserver and scheduler
## Start the Airflow webserver

#!/bin/bash
## Shebang to specify the script interpreter

set -e
## Exit immediately if a command exits with a non-zero status

echo "Starting script execution..."
## a message indicating the start of script execution

if [ -e "/opt/airflow/requirements.txt" ]; then
    ## Check if the requirements.txt file exists in the specified directory
    echo "Installing Python packages from requirements.txt..."
    ## a message indicating the installation of Python packages
    python -m pip install --upgrade pip
    ## Upgrade pip
    pip install -r requirements.txt
    ## Install packages listed in requirements.txt
fi

if [ ! -f "/opt/airflow/airflow.db" ]; then
    ## Check if the Airflow database file does not exist
    echo "Initializing Airflow database..."
    ##  a message indicating the initialization of the Airflow database
    airflow db init
    ## Initialize the Airflow database
    echo "Creating Airflow user..."
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
## a message indicating the upgrade of the Airflow database
airflow db upgrade
## Upgrade the Airflow database

echo "Starting Airflow webserver and scheduler..."
## a message indicating the start of the Airflow webserver and scheduler
exec airflow webserver
## Start the Airflow webserver

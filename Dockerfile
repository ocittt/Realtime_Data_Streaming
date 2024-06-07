FROM apache/airflow:2.6.0-python3.9

# Copy requirements and script files with the correct ownership
COPY --chown=airflow:airflow requirements.txt /opt/airflow/requirements.txt
COPY --chown=airflow:airflow airflow_script/eltscript.sh /opt/airflow/airflow_script/eltscript.sh

# Make the script executable
USER root
RUN chmod +x /opt/airflow/airflow_script/eltscript.sh
USER airflow

# Install necessary Python packages as airflow user
RUN pip install --user -r /opt/airflow/requirements.txt

ENTRYPOINT ["/opt/airflow/airflow_script/eltscript.sh"]

import logging
from datetime import datetime

from cassandra.auth import PlainTextAuthenticator
from cassandra.cluster import Cluster
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col

def create_keyspace(session):
    # create space here


def create_table(session):
    # create table here


def insert_data(session):
    # insertion here


def create_spark_connection():
    # createing spark connection

    s_conn =  


    try:
        s_conn = SparkSession.builder \
            .appName('SparkDatabStreaming') \
            .config('spark.jars.packages', "com.datastax.spark:spark-cassandra-connector_2.13:3.5.1,"
                                           "org.apache.spark:spark-sql-kafka-0-10_2.13:4.0.0-preview1") \
            .config('spark.cassandra.connection.host', 'localhost') \
            .getOrCreate()
        
        s_conn.sparkContent.setLogLevel("ERROR")
        logging.info("Spark Connection Created Successfully!")
    except Exception as e:
        logging.error(f"Couldn't Create the Spark session due to exception {e}")

    return s_conn

def create_cassandra_connection():
    # creating cassandra connection

    session = None

    try:
        cluster = Cluster(['localhost'])
        
        session = cluster.connect()
    except Exception as e:
        logging.error(f"Couldn't Create the Cassandra Connection due to {e}")
    return session


if __name__ == "__main__":
    spark_conn = create_spark_connection()
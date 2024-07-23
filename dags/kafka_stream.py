from datetime import datetime
## Import the datetime class from the datetime module
from airflow import DAG 
## Import the DAG class from the airflow module
from airflow.operators.python import PythonOperator
## Import the PythonOperator class from the airflow.operators.python module

default_args = {
    'owner': 'airocit',
    'start_date': datetime(2024, 6, 28, 10, 00)
}
## Define default arguments for the DAG

def get_data():
    import requests
    ## Import the requests module for making HTTP requests
    
    res = requests.get("https://randomuser.me/api/")
    ## Make a GET request to the specified API
    res = res.json()
    ## Parse the response as JSON
    res = res['results'][0]
    ## Extract the first result from the response
    # print(json.dumps(res, indent=3))

    return res
    ## Return the extracted result

def format_data(res):
    data = {}
    ## Initialize an empty dictionary to store formatted data
    location = res['location']
    ## Extract the location information from the response
    
    data['first_name'] = res['name']['first']
    ## Store the first name in the data dictionary
    data['last_name'] = res['name']['last']
    ## Store the last name in the data dictionary
    data['gender'] = res['gender']
    ## Store the gender in the data dictionary
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    ## Store the formatted address in the data dictionary
    data['post_code'] = location['postcode']
    ## Store the postal code in the data dictionary
    data['email'] = res['email']
    ## Store the email in the data dictionary
    data['dob'] = res['dob']['date']
    ## Store the date of birth in the data dictionary
    data['registered_date'] = res['registered']['date']
    ## Store the registration date in the data dictionary
    data['phone'] = res['phone']
    ## Store the phone number in the data dictionary
    data['picture'] = res['picture']['medium']
    ## Store the picture URL in the data dictionary
    
    return data
    ## Return the formatted data

def stream_data():
    import json
    ## Import the json module for handling JSON data
    from kafka import KafkaProducer
    ## Import the KafkaProducer class from the kafka module
    import time
    ## Import the time module for time-related functions
    import logging
    ## Import the logging module for logging errors
    # res = get_data()
    # res = format_data(res)

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    ## Initialize a KafkaProducer to send messages to the specified Kafka broker with a maximum blocking time of 5000 ms
    curr_time = time.time()
    ## Get the current time

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        ## Continue the loop for 1 minute

        try:
            res = get_data()
            ## Get data from the API
            res = format_data(res)
            ## Format the data

            producer.send('users_created', json.dumps(res).encode('utf-8'))
            ## Send the formatted data to the 'users_created' topic on Kafka
        except Exception as e:
            logging.error(f'An error occured: {e}')
            ## Log any errors that occur
            continue
            ## Continue the loop even if an error occurs

with DAG('user_automation',
         default_args=default_args,
         schedule_interval='@daily',
         catchup=False) as dag:
    ## Define a DAG named 'user_automation' with the specified default arguments and a daily schedule

    streaming_task = PythonOperator(
        task_id='stream_data_from_api',
        python_callable=stream_data
    )
    ## Define a PythonOperator task named 'stream_data_from_api' that calls the stream_data function


# stream_data()
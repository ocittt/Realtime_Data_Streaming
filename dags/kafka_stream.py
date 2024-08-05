from datetime import datetime
from airflow import DAG 
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airocit',
    'start_date': datetime(2024, 6, 28, 10, 00)
}
## Define default arguments for the DAG

def get_data():
    import requests
    
    res = requests.get("https://randomuser.me/api/")
    ## Make a GET request to the specified API
    
    res = res.json()
    res = res['results'][0]
    ## Parse the response as JSON
    ## Extract the first result from the response
    
    
    # print(json.dumps(res, indent=3))

    return res
    ## Return the extracted result

def format_data(res):
    data = {}
    location = res['location']
    ## Initialize an empty dictionary to store formatted data
    ## Extract the location information from the response
    
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, " \
                      f"{location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']

    
    return data
    ## Return the formatted data

def stream_data():
    import json
    from kafka import KafkaProducer
    import time
    import logging
    
    # res = get_data()
    # res = format_data(res)

    producer = KafkaProducer(bootstrap_servers=['broker:29092'], max_block_ms=5000)
    curr_time = time.time()
    ## Initialize a KafkaProducer to send messages to the specified Kafka broker with a maximum blocking time of 5000 ms
    ## Get the current time

    while True:
        if time.time() > curr_time + 60: #1 minute
            break
        ## Continue the loop for 1 minute

        try:
            res = get_data()
            res = format_data(res)

            producer.send('users_created', json.dumps(res).encode('utf-8'))
            ## Send the formatted data to the 'users_created' topic on Kafka
            
        except Exception as e:
            logging.error(f'An error occured: {e}')
            continue
            ## Log any errors that occur
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
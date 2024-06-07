from datetime import datetime
import json
from airflow import DAG 
from airflow.operators.python import PythonOperator

default_args = {
    'owner': 'airocit',
    'start_date': datetime(2024, 6, 7, 16, 0)
}

def get_data():
    import requests
    res = requests.get("https://randomuser.me/api/")
    res = res.json()
    res = res['results'][0]
    print(json.dumps(res, indent=3))
    return res

def format_data(res):
    data = {}
    location = res['location']
    data['first_name'] = res['name']['first']
    data['last_name'] = res['name']['last']
    data['gender'] = res['gender']
    data['address'] = f"{str(location['street']['number'])} {location['street']['name']}, {location['city']}, {location['state']}, {location['country']}"
    data['post_code'] = location['postcode']
    data['email'] = res['email']
    data['dob'] = res['dob']['date']
    data['registered_date'] = res['registered']['date']
    data['phone'] = res['phone']
    data['picture'] = res['picture']['medium']
    return data

def stream_data():
    from kafka import KafkaProducer
    import time
    res = get_data()
    res = format_data(res)
    producer = KafkaProducer(bootstrap_servers=['broker:9092'], max_block_ms=5000)
    producer.send('users_created', json.dumps(res).encode('utf-8'))
    producer.flush()
    producer.close()

with DAG(
    'user_automation',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:

    streaming_task = PythonOperator(
       task_id='stream_data_from_api',
       python_callable=stream_data
    )

# stream_data()
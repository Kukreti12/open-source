from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner': 'your_name',
    'start_date': datetime(2023, 7, 6),
}

def print_current_date():
    current_date = datetime.now().strftime("%Y-%m-%d")
    print(f"Current date is: {current_date}")

with DAG(
    'print_current_date_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False
) as dag:
    task = PythonOperator(
        task_id='print_current_date_task',
        python_callable=print_current_date
    )

    task

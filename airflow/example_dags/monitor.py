from airflow import DAG
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

dag = DAG('file_move_dag', start_date=datetime(2023, 6, 12), schedule_interval='* * * * *')

source_directory = '/mnt/shared/DFM/quarantine/'
target_directory = '/mnt/shared/DFM/bronze'

# File sensor to monitor the source directory for the new file
file_sensor_task = FileSensor(
    task_id='file_sensor_task',
    filepath=source_directory,
    poke_interval=10,  # Adjust the interval as per your requirement
    dag=dag
)

# Bash operator to move the file from source to target directory
move_file_task = BashOperator(
    task_id='move_file_task',
    bash_command=f'mv {source_directory}/{{{{ task_instance.xcom_pull("file_sensor_task") }}}}'
                f' {target_directory}',
    dag=dag
)

file_sensor_task >> move_file_task
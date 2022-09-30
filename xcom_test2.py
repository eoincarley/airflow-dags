from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models.baseoperator import BaseOperator


class HelloOperator(BaseOperator):
    def __init__(self, name: str, property: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.property = property

    def execute(self, context):
        message = f"Hello {self.name}"
        print(self.property)
        print(message)
        return message

def print_hello(**kwargs):

    ti = kwargs['ti']
    ti.xcom_push(key='someobject', value='test')
    return 'Hello world from first Airflow DAG!'

###################################################



with DAG(
    dag_id = 'hello_world', 
    description='Hello World DAG',
    schedule_interval='0 12 * * *',
    start_date=datetime(2017, 3, 20),
    catchup=False
) as dag:

    hello_operator = PythonOperator(task_id='hello_task', python_callable=print_hello)

    hello_task = HelloOperator(task_id="sample-task", name="foo_bar", property=ti.xcom_pull(task_ids='Task1', key='someobject'))


hello_operator >> hello_task
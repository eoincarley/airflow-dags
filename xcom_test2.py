from datetime import datetime
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from airflow.models.baseoperator import BaseOperator

from airflow.models import TaskInstance



class HelloOperator(BaseOperator):
    def __init__(self, name: str, property: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.name = name
        self.property = property
        self.dag = kwargs['dag']
        
        operator_instance = self.dag.get_task('hello_task')
        task_status = TaskInstance(operator_instance)

        print(type_status)

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

    hello_task = HelloOperator(task_id="sample-task", name="foo_bar", dag = dag, property='Some sameple text')


hello_operator >> hello_task
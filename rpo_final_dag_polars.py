import datetime as dt
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.base_hook import BaseHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from sqlalchemy import create_engine
from airflow.utils.dates import days_ago

_CONN_ID = 'postgres_sql'
_SCHEMA = 'rpo_etl'
_TABLE = 'rpo_data'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': dt.datetime(2025,3,16),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
}

dag = DAG(
    'RPO_final_dag',
    default_args=default_args,
    description='RPO process',
    schedule_interval='@once',
)

def ETL():
    from RPO_etl_polars import rpo
    supplier, part, inspect, desc, stats, fact = rpo(exelFile='/opt/airflow/data/dummy.xlsx')
    conn = BaseHook.get_connection('postgres_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    supplier.write_database('suppliers_dimension', engine, if_table_exists='append')
    part.write_database('parts_dimension', engine, if_table_exists='append')
    inspect.write_database('inspection_dimension', engine, if_table_exists='append')
    desc.write_database('descriptions_dimension', engine, if_table_exists='append')
    stats.write_database('statistic_dimension', engine, if_table_exists='append')
    fact.write_database('fact_temp', engine, if_table_exists='replace')

with dag:
    create_table= SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id=_CONN_ID,
        sql="rpoquery.sql"
    )
    run_etl = PythonOperator(
        task_id='run_etl',
        python_callable=ETL,
        dag=dag,
    )
    add_to_fact= SQLExecuteQueryOperator(
        task_id='add_to_fact',
        conn_id=_CONN_ID,
        sql="rpo_add_to_fact.sql"
    )

    create_table >> run_etl >> add_to_fact
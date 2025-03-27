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
    'retry_delay': dt.timedelta(minutes=1)
}

dag = DAG(
    'RPO_final_dag',
    default_args=default_args,
    description='RPO process',
    schedule_interval=dt.timedelta(minutes=50),
)

def ETL():
    from dags.RPO_etl_backup import rpo
    df=rpo()
    #print(df)
    conn = BaseHook.get_connection('postgres_sql')
    engine = create_engine(f'postgresql://{conn.login}:{conn.password}@{conn.host}:{conn.port}/{conn.schema}')
    df.to_sql('rpo_data', engine, if_exists='replace')

with dag:
    create_table= SQLExecuteQueryOperator(
        task_id='create_table',
        conn_id=_CONN_ID,
        sql="""
            CREATE TABLE IF NOT EXISTS rpo_data(
            Critical_Parameter_Numbers VARCHAR(200),
            Description VARCHAR(200),
            CP_Type VARCHAR(200),
            Nominal decimal(200),
            Tolerance decimal(200),
            USL decimal(200),
            LSL decimal(200),
            MC_Upper_Limit decimal(200),
            MC_Lower_Limit decimal(200),
            Mean decimal(200),
            MC_percent_Error decimal(200),
            Stdev decimal(200),
            UCL_of_HVM_Cpk_Estimate decimal(200),
            HVM_Cpk_Point_Estimate decimal(200),
            LCL_of_HVM_Cpk_Estimate decimal(200),
            Min decimal(200),
            Max decimal(200),
            Range decimal(200),
            Count decimal(200),
            Sample_1 decimal(200),
            Sample_2 decimal(200),
            Sample_3 decimal(200),
            Sample_4 decimal(200),
            Sample_5 decimal(200),
            Sample_6 decimal(200),
            Sample_7 decimal(200),
            Sample_8 decimal(200),
            Sample_9 decimal(200),
            Sample_10 decimal(200),
            Sample_11 decimal(200),
            Sample_12 decimal(200),
            Sample_13 decimal(200),
            Sample_14 decimal(200),
            Sample_15 decimal(200),
            Sample_16 decimal(200),
            Sample_17 decimal(200),
            Sample_18 decimal(200),
            Sample_19 decimal(200),
            Sample_20 decimal(200),
            Sample_21 decimal(200),
            Sample_22 decimal(200),
            Sample_23 decimal(200),
            Sample_24 decimal(200),
            Sample_25 decimal(200),
            Sample_26 decimal(200),
            Sample_27 decimal(200),
            Sample_28 decimal(200),
            Sample_29 decimal(200),
            Sample_30 decimal(200),
            Sample_31 decimal(200),
            Sample_32 decimal(200),
            CONSTRAINT primary_key_constraint PRIMARY KEY (Critical_Parameter_Numbers)
        )
        """,
        params={"schema": _SCHEMA, "table": _TABLE}
    )
    run_etl = PythonOperator(
        task_id='run_etl',
        python_callable=ETL,
        dag=dag,
    )

    create_table >> run_etl
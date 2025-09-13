import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))                

import os
from pendulum import datetime, duration
from airflow.sdk import task
from projects.core.elt_core import LoadData
from core.elt_core import ExtractData
from core.elt_core import TransformData
from typing import Type, Collection, Dict

class PipelineConstructor:
    def __init__(self) -> None:
        pass

    def set_dag_settings(self,
                        dag_name: str,
                        dag_description: str,
                        start_date: str,
                        schedule_interval: str,
                        tags: Collection[str] = None,
                        recursive: bool = False,
                        owner: str = 'Data_Owner',
                        retries_qtd: int = 3,
                        retries_delay_minutes: int = 1,
                        ) -> Dict:
        """Define the settings for the DAG.

        Args:
            dag_name (str): Name of the DAG.
            dag_description (str): Description of the DAG.
            start_date (str): Start date of the DAG in the format 'YYYY-MM-DD'.
            schedule_interval (str): Schedule interval for the DAG (e.g., '0 0 * * 1-5').
            tags (Collection[str], optional): Tags for the DAG. Defaults to None.
            recursive (bool, optional): Whether the DAG should catch up on missed runs. Defaults to False.
            owner (str, optional): Owner of the DAG. Defaults to 'Data_Owner'.
            retries_qtd (int, optional): Number of retries in case of failure. Defaults to 3.
            retries_delay_minutes (int, optional): Delay in minutes between retries. Defaults to 1.
        Returns:
            dict: Dictionary containing the settings for the DAG.
        """

        year = int(start_date[:4])
        month = int(start_date[5:7])
        day = int(start_date[-2:])
            
        default_args = self._set_dag_retries_options(owner=owner, retries_qtd=retries_qtd, retries_delay_minutes=retries_delay_minutes)

        settings = {
                'dag_id': dag_name,
                'description': dag_description,
                'start_date': datetime(year=year, month=month, day=day, tz='America/Sao_Paulo'),
                'schedule': schedule_interval,
                'catchup': recursive,
                'tags': tags,
                'default_args': default_args,
        }
        return settings
    
    @staticmethod
    def _set_dag_retries_options(owner: str, retries_qtd: int, retries_delay_minutes: int) -> Dict:
        """Define the retry options for the DAG.

        Args:
            owner (str): Owner of the DAG.
            retries_qtd (int): Number of retries in case of failure.
            retries_delay_minutes (int): Delay in minutes between retries.
        Returns:
            Dict: Dictionary containing the retry options for the DAG.
        """
        default_args={
            'owner': owner,
            'retries': retries_qtd,
            'retry_delay': duration(minutes=retries_delay_minutes),
            'retry_exponential_backoff': True,
            'max_retry_delay': duration(hours=2),
        }
        return default_args

    @staticmethod
    def etl_tasks(extract_class: Type[ExtractData],
                transform_class: Type[TransformData], 
                load_class: Type[LoadData],
                ):
        """Method to create ETL tasks in the DAG.
        
        Args:
            extract_class (Type[ExtractData]): Class that implements the ExtractData interface.
            transform_class (Type[TransformData]): Class that implements the TransformData interface.
            load_class (Type[LoadData]): Class that implements the LoadData interface.
        """
        @task(task_id='Extract_Data')
        def task_extract(logical_date):
            """Task to perform data extraction."""
            extract = extract_class()
            return extract.extract_data(exec_date=logical_date)

        @task(task_id='Transform_Data')
        def task_transform(logical_date):
            """Task to perform data transformation."""
            transform = transform_class()
            return transform.transform_data(exec_date=logical_date)

        @task(task_id='Load_Data')
        def task_insert_data_into_database():
            """Task to perform data loading into the database."""
            load = load_class()
            return load.load_data()

    # ---------------------------------------------------------------------------
        # Declare dependencies
        extract = task_extract()
        transform = task_transform(extract)
        load = task_insert_data_into_database(transform)

        extract >> transform
        transform >> load

                
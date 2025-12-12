import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))                

import importlib.util
from airflow.sdk import dag  # alterado de airflow.decorators para airflow.sdk
from projects.core.pipeline import PipelineConstructor

data_pipeline = PipelineConstructor()

data_acquistion_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'projects', 'get_data_project'))

for root, dirs, files in os.walk(data_acquistion_path):
    for file in files:
        if file == 'dag_info.py':
            full_path = os.path.join(root, file)
            module_name = os.path.splitext(file)[0]

            spec = importlib.util.spec_from_file_location(module_name, full_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[module_name] = module
            spec.loader.exec_module(module)

            if hasattr(module, 'main_dag'):
                
                dag_info = module.main_dag


                dag_settings = data_pipeline.set_dag_settings(dag_name=dag_info['dag_name'],
                                                            dag_description=dag_info['dag_description'],
                                                            start_date=dag_info['start_date'],
                                                            schedule_interval=dag_info['schedule_interval'],
                                                            tags= dag_info['tags'] if 'tags' in dag_info else None)


                @dag(**dag_settings)
                def pipeline():
                    data_pipeline.etl_tasks(extract_class=dag_info['extract_class'],
                                            transform_class=dag_info['transform_class'],
                                            load_class=dag_info['load_class'],
                                            )

                pipeline()
            else:
                print(f"{file}: 'main_dag' not found")
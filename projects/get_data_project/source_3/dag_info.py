from projects.get_data_project.source_3.extract import ExtractDataSource3
from projects.get_data_project.source_3.transform import TransformDataSource3
from projects.get_data_project.source_3.load import LoadDataSource3

main_dag = {
        'dag_name': 'Source_Database',
        'dag_description': 'Pipeline to extract, transform, and load data from Source 3',
        'start_date': '2025-09-01',
        'schedule_interval': '*/2 8-17 * * 1-5',
        'extract_class': ExtractDataSource3,
        'transform_class': TransformDataSource3,
        'load_class': LoadDataSource3,
        'tags': ['tag_2', 'source_database'],
    }
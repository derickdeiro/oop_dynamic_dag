from projects.get_data_project.source_2.extract import ExtractDataSource2
from projects.get_data_project.source_2.transform import TransformDataSource2
from projects.get_data_project.source_2.load import LoadDataSource2

main_dag = {
        'dag_name': 'Source_Database',
        'dag_description': 'Pipeline to extract, transform, and load data from Source 3',
        'start_date': '2025-09-01',
        'schedule_interval': '0-59/2 * * *',
        'extract_class': ExtractDataSource2,
        'transform_class': TransformDataSource2,
        'load_class': LoadDataSource2,
        'tags': ['tag_2', 'source_database'],
    }
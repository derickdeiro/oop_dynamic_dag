from projects.get_data_project.source_1.extract import ExtractDataSource1
from projects.get_data_project.source_1.transform import TransformDataSource1
from projects.get_data_project.source_1.load import LoadDataSource1

main_dag = {
        'dag_name': 'Source_API',
        'dag_description': 'Pipeline to extract, transform, and load data from Source 1',
        'start_date': '2025-08-01',
        'schedule_interval': '@monthly',
        'extract_class': ExtractDataSource1,
        'transform_class': TransformDataSource1,
        'load_class': LoadDataSource1,
        'tags': ['tag_1', 'source_api'],
    }
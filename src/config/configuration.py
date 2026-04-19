## CONFIGURATION MANAGER ## 
from src.utils.utils import read_yaml, create_directories

# DATA INGESTION 
from src.entity.entity import DataIngestionConfig

# DATA VALIDATION 

class ConfigurationManager: 
    def __init__(self, 
                 config='config/config.yaml',
                 params='params.yaml',
                 schema='schema.yaml'):
        
        # Note: YAML FILES MUST NOT BE EMPTY FOR THIS TO WORK
        self.config = read_yaml(config)
        self.params = read_yaml(params)
        self.schema = read_yaml(schema)

        create_directories([self.config.artifact_dir])

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_artifact = DataIngestionConfig(
            root_dir=config.root_dir,
            artifact_path=config.artifact_path,
            path_name=config.path_name
            
        )
        
        return data_ingestion_artifact
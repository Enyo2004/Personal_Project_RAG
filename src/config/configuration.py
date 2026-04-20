## CONFIGURATION MANAGER ## 
import os 
from src.utils.utils import read_yaml, create_directories

# DATA INGESTION 
from src.entity.entity import (DataIngestionConfig,
                               DataTransformationConfig)

# import the constants from configuration
from src.config import *

class ConfigurationManager: 
    def __init__(self, 
                 config=CONFIG_YAML,
                 params=PARAMS_YAML,
                 schema=SCHEMA_YAML):
        
        # Note: YAML FILES MUST NOT BE EMPTY FOR THIS TO WORK
        self.config = read_yaml(config)
        self.params = read_yaml(params)
        self.schema = read_yaml(schema)

        create_directories([self.config.artifact_dir])

    '''Data ingestion Config'''
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion

        create_directories([config.root_dir])

        data_ingestion_artifact = DataIngestionConfig(
            root_dir=config.root_dir,
            artifact_path=config.artifact_path,
            path_name=config.path_name
            
        )
        
        return data_ingestion_artifact
    
    """Data Transformation Config"""
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation 

        create_directories([os.path.join(config.artifact_path, config.root_dir)])

        data_transformation_config = DataTransformationConfig(
            source=config.source,
            root_dir=config.root_dir,
            path_name=config.path_name,
            artifact_path=config.artifact_path,
            llm=config.llm
        )

        return data_transformation_config


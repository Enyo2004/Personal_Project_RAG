## CONFIGURATION MANAGER ## 
import os 
from pathlib import Path 

from src.utils.utils import read_yaml, create_directories

# DATA INGESTION 
from src.entity.entity import (DataIngestionConfig,
                               DataTransformationConfig,
                               VectorDBConfig,
                               ResponseLLMConfig)

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
    

    """Vector DB Config"""
    def get_vector_db_config(self) -> VectorDBConfig:
        
        # config keys
        config = self.config.vector_db
        
        create_directories([Path(config.artifact_path).parent])
        
        # params keys 
        splitter = self.params.CharacterSplitter

        bmRetriever = self.params.bm25

        reranker = self.params.reranker

        hybrid_retriever = self.params.hybrid_retriever

        # get the config 
        vector_db_config = VectorDBConfig(
            source=config.source,
            path_name=config.path_name,
            
            embedding_name=config.embedding_name,
            artifact_path=config.artifact_path, 

            # splitter 
            chunk_size=splitter.chunk_size,
            chunk_overlap=splitter.chunk_overlap,

            # bm25 retriever 
            k=bmRetriever.k, 

            # reranker 
            top_n=reranker.top_n,

            # hybrid_retriever 
            weights=hybrid_retriever.weights,
        )

        return vector_db_config

    """Response LLM config"""
    def get_llm_response_config(self,) -> ResponseLLMConfig:
        
        config = self.config.response_llm

        create_directories([Path(config.artifact_path).parent])

        llm_response_config = ResponseLLMConfig(
            llm=config.llm,
            artifact_path=config.artifact_path
        )

        return llm_response_config

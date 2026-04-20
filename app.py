### TRY THE DATA INGESTION PIPELINE ### 

"""Data ingestion"""
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline

"""Data Transformation"""
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline

try: 

    data_ingestion_pipeline = DataIngestionPipeline()

    data_ingestion_pipeline.initiate_data_ingestion()
    
    data_transformation_pipeline = DataTransformationPipeline()

    data_transformation_pipeline.initiate_data_transformation()
    
    
except Exception as e: 
    raise e 

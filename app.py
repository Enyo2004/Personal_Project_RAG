### TRY THE DATA INGESTION PIPELINE ### 

"""Data ingestion"""
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline

"""Data Transformation"""
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline

"""Vector DB"""
from src.pipeline.vector_db_pipeline import VectorDBPipeline

try: 
    '''Data Ingestion'''
    data_ingestion_pipeline = DataIngestionPipeline()

    data_ingestion_pipeline.initiate_data_ingestion()
    
    '''Data transformation'''
    data_transformation_pipeline = DataTransformationPipeline()

    data_transformation_pipeline.initiate_data_transformation()
    
    '''Vector DB'''
    vector_db_pipeline = VectorDBPipeline()

    weaviate_client, retriever = vector_db_pipeline.initiate_vector_db()

    print(weaviate_client, retriever)

except Exception as e: 
    raise e 

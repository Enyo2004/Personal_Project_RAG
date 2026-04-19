### TRY THE DATA INGESTION PIPELINE ### 

"""Data ingestion"""
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline


try: 
    data_ingestion_pipeline = DataIngestionPipeline()

    data_ingestion_pipeline.start_data_ingestion()

except Exception as e: 
    raise e 

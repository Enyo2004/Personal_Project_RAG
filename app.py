### TRY THE DATA INGESTION PIPELINE ### 

"""Data ingestion"""
from src.pipeline.data_ingestion_pipeline import DataIngestionPipeline

"""Data Transformation"""
from src.pipeline.data_transformation_pipeline import DataTransformationPipeline

"""Vector DB"""
from src.pipeline.vector_db_pipeline import VectorDBPipeline

"""Response LLM"""
from src.pipeline.response_llm_pipeline import ResponseLLMPipeline

class CompletePipeline:
    def __init__(self, ):
        pass 

    def workflow(self,):
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


            '''Response LLM'''
            response_llm_pipeline = ResponseLLMPipeline(
                vector_db=weaviate_client,
                retriever=retriever,
            )
            
            # return the llm response object
            return response_llm_pipeline

        except Exception as e: 
            raise e 

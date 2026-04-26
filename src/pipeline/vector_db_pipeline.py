## provide the pipeline 

# get the configuration manager 
from src.config.configuration import ConfigurationManager

# get the vector db component (functionality)
from src.components.vector_db import VectorDB 

from langchain_weaviate import WeaviateVectorStore
from langchain_classic.retrievers import EnsembleRetriever

class VectorDBPipeline: 
    def __init__(self, ): 
        pass 

    def initiate_vector_db(self,) -> tuple[WeaviateVectorStore, EnsembleRetriever]:
        try:
            ## create the pipeline 
            config = ConfigurationManager()

            vector_db_config = config.get_vector_db_config()

            vector_db = VectorDB(vector_db_config)

            weaviate_client, retriever = vector_db.start_vector_db()

            return weaviate_client, retriever
        
        except Exception as e:
            raise e
        
## provide the pipeline 

# get the configuration manager 
from src.config.configuration import ConfigurationManager

# get the vector db component (functionality)
from src.components.vector_db import VectorDB 


class VectorDBPipeline: 
    def __init__(self, ): 
        pass 

    def initiate_vector_db(self, user_message:str) -> str:
        try:
            ## create the pipeline 
            config = ConfigurationManager()

            vector_db_config = config.get_vector_db_config()

            vector_db = VectorDB(vector_db_config)

            response = vector_db.start_vector_db(query=user_message)

            return response
        
        except Exception as e:
            raise e
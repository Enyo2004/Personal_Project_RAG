# import the Configuration manager 
from src.config.configuration import ConfigurationManager

# import the Data Transformation component 
from src.components.response_llm import ResponseLLM

from src.utils.logger_artifact import logger

from langchain_weaviate import WeaviateVectorStore
from langchain_classic.retrievers import ContextualCompressionRetriever

class ResponseLLMPipeline:
    def __init__(self, vector_db:WeaviateVectorStore, retriever:ContextualCompressionRetriever):
        self.vector_db = vector_db
        self.retriever = retriever

    def initiate_llm_response(self, query:str):
        try:
            logger.info("Starting Data LLM Response Phase")
            # run the pipeline 
            config = ConfigurationManager()

            llm_response_config = config.get_llm_response_config()

            llm_response = ResponseLLM(
                config=llm_response_config,
                weaviate_vector_db=self.vector_db,
                reranker_retriever=self.retriever
            )

            llm_response_answer= llm_response.llm_response(user_message=query)

            logger.info("LLM response loaded successfullly in the .txt file")            

            return llm_response_answer
        
        except Exception as e: 
            raise e
        



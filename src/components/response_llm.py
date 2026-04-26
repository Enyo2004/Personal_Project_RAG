from pathlib import Path
import os 

from src.config.configuration import ResponseLLMConfig
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage

import weaviate 

from langchain_openai import ChatOpenAI
from langchain_weaviate import WeaviateVectorStore
from langchain_classic.retrievers import ContextualCompressionRetriever
 
from src.utils.logger_artifact import logger


"""Response LLM component (functionalities)"""
class ResponseLLM: 
    def __init__(self,
                 # pass arguments into the class
                 weaviate_vector_db:WeaviateVectorStore,
                 reranker_retriever:ContextualCompressionRetriever,

                 config=ResponseLLMConfig,
                 ):
        
        self.config = config

        # provide the llm client
        self.client_llm = ChatOpenAI(
            model="llama3.1-8b",
            base_url= os.getenv("CEREBRAS_BASE_URL"),
            api_key=os.getenv("CEREBRAS_API_KEY"),
            max_retries=3,
        )  


        # provide the retriever to use 
        self.reranker_retriever = reranker_retriever

        # provide the vector db to use 
        self.weaviate_vector_db = weaviate_vector_db

        # create the response file 
        self.response_file = Path(self.config.artifact_path)
        self.response_file.touch()

        logger.info("Connecting to weaviate")
        # connection 
        self.connection = weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("CLUSTER_URL"), # rest endpoint (temporal cluster) get it from .env file
            auth_credentials=weaviate.classes.init.Auth.api_key(api_key=os.getenv("WEAVIATE_TEMPORAL_API_KEY")) # api key (create one first and add to .env file)
        )
        logger.info("Successfully connected to weaviate")

    def get_context(self, user_message:str, ) -> str: 
        """Return the response of the llm using the retriever"""
        logger.info(f"Getting context from the user message: {user_message}")
        # retrieve the info (documents)
        retrieved_info = self.reranker_retriever.invoke(input=user_message)

        # get the string information from the documents 
        context = ""
        for info in retrieved_info:
            context+=info.page_content  

        logger.info(f"Successfully got the context from the user message: {user_message}")
        return context 
    
    def llm_response(self, user_message:str) -> str:
        with self.connection as client: # call the client, do something and close it 
            # get the context
            context = self.get_context(user_message=user_message)


            # get the response of the llm 
            response = self.client_llm.invoke(
                                input=[SystemMessage(content=f"You are a helpful spiritual assistant FLUENT in ENGLISH and SPANISH, that answers the questions IN SPANISH according to these context: {context}"),
                                        AIMessage(content="Aqui te proporciono la informacion que ocupas:"),
                                        HumanMessage(content=user_message)] 
                            )
            
            # append the history to the list 
            #self.history.append(HumanMessage(content=user_message))
            #self.history.append(AIMessage(response.content))
            logger.info(f"Appending the messages of the user and AI in the {self.response_file.name} file")
            with open(self.response_file, mode='a') as file:
                file.write(f"User question: {user_message}\n")
                file.write(f"LLM answer: {response.content}")
            logger.info(f"User and AI messages appended in the {self.response_file.name} file")      

            return response.content


import os
from pathlib import Path

# Make sure your Langchain/Cerebras imports are here
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from langchain_openai import ChatOpenAI

from langchain_classic.retrievers import ContextualCompressionRetriever
from langchain_weaviate import WeaviateVectorStore

from src.config.configuration import ResponseLLMConfig

from src.utils.logger_artifact import logger

from dotenv import load_dotenv

# load the weaviate client 
class ResponseLLM: 
    def __init__(self,
                 weaviate_vector_db:WeaviateVectorStore, 
                 reranker_retriever:ContextualCompressionRetriever,
                 config: ResponseLLMConfig,
                 ):

        load_dotenv(override=True)
        self.config = config

        # provide the llm client
        self.client_llm = ChatOpenAI(
            model="openai.gpt-oss-safeguard-120b",
            base_url=f"https://bedrock-mantle.{os.getenv("AWS_REGION_NAME")}.api.aws/v1",
            api_key=os.getenv("AWS_API_KEY"),
            max_retries=3,
            temperature=0.8,
            max_completion_tokens=3000
        )  

        # provide the retriever and vector db
        self.reranker_retriever = reranker_retriever
        self.weaviate_vector_db = weaviate_vector_db

        # create the response file 
        self.response_file = Path(self.config.artifact_path)
        self.response_file.touch()
        
        # Your reranker_retriever already handles the DB connection.

    def get_context(self, user_message: str) -> str: 
        """Return the context using the retriever"""
        logger.info(f"Getting context from the user message: {user_message}")
        
        # retrieve the info (documents)
        retrieved_info = self.reranker_retriever.invoke(input=user_message)

        # get the string information from the documents 
        context = ""
        for info in retrieved_info:
            context += info.page_content  

        logger.info(f"Successfully got the context from the user message: {user_message}")
        return context 
    
    def llm_response(self, user_message: str) -> str:

        # 1. Get the context
        context = self.get_context(user_message=user_message)

        # 2. Get the response of the llm 
        response = self.client_llm.invoke(
            input=[
                SystemMessage(content=f"""You are a helpful spiritual assistant for this WOMAN: {os.getenv("PERSON_NAME")} 
                              AVOID USING PHRASES THAT ARE USED BY CHATBOTS, MAKE THIS CONVERSATION VERY HUMAN, PROVIDE MYSTICAL PHRASES IN MEXICAN SPANISH
                              TRY USING MEXICAN "DICHOS" WHEN APPROPRIATE
                              ALWAYS MENTION THIS NAME {os.getenv("PERSON_NAME")} WHEN PROVIDING AN ANSWER, TALK IN A REALLLY SPIRITUAL FORM WITHOUT EXAGERATING, and talk as a FEMALE assistant of a good, friendly witch (FRIENDLY BUT SPIRITUAL TONE)
                              YOU are FLUENT in ENGLISH and SPANISH, that answers the questions IN SPANISH according to these context: {context} 
                              You provide your answers in an explainable way but concise and always direct yourself with respect, also propose tips in the topic asked, ALWAYS ANSWER IN SPANISH
                              """),
                AIMessage(content="Saludo cordial:"),
                HumanMessage(content=user_message)
            ] 
        )
        
        # 3. Save to file
        logger.info(f"Appending the messages of the user and AI in the {self.response_file.name} file")
        with open(self.response_file, mode='a', encoding='utf-8') as file:
            file.write(f"User question: {user_message}\n")
            file.write(f"LLM answer: {response.content}\n")
        logger.info(f"User and AI messages appended in the {self.response_file.name} file")      

        return response.content
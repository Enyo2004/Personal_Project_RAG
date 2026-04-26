# vector db component # 
from typing import List, Any

### imports ### 
import os 
from dotenv import load_dotenv 

# get the files path 
import glob 
from pathlib import Path

# load the documents 
from langchain_community.document_loaders import DirectoryLoader # load the directory 
from langchain_community.document_loaders.markdown import UnstructuredMarkdownLoader # load the markdown files 

# recursive text splitters (chunk creation)
from langchain_text_splitters import RecursiveCharacterTextSplitter 

# embeddings used 
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

# vector store usage 
import weaviate
from langchain_weaviate import WeaviateVectorStore
from langchain_community.retrievers import BM25Retriever # keyword retriever 
from langchain_classic.retrievers import EnsembleRetriever # ensemble the retrievers

## use of rerankers of chunks 
from langchain_community.document_compressors.flashrank_rerank import FlashrankRerank
from langchain_classic.retrievers import ContextualCompressionRetriever 


# llm usage to retrieve from the documents 
from langchain_openai.chat_models import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage  # system, user, assistant message 


### LOAD THE ENTITY CONFIG ### 
from src.entity.entity import VectorDBConfig


# load the logger # 
from src.utils.logger_artifact import logger

### instantiate the component class ### 
class VectorDB: 
    def __init__(self,
                 config=VectorDBConfig):
        
        load_dotenv(override=True)
        self.config = config 
        
        # create the path object 
        self.response_file_txt = Path(self.config.artifact_path)
        
        # create the file within the directory
        self.response_file_txt.touch(exist_ok=True)

        
    def load_files(self) -> List[Any]: 
        # Loading the files 
        
        logger.info(f"Loading files from: {self.config.source}")
        files_to_load = DirectoryLoader(
            path=self.config.source,
            glob=self.config.path_name,

            loader_cls=UnstructuredMarkdownLoader,
            loader_kwargs={"encoding":"utf-8"},
            
            show_progress=True,
            )
        
        loaded_files = files_to_load.load()
        
        
        ## Add metadata 
        for file in loaded_files:
            ## add the document name to the metadata 
            file.metadata['topic'] = str(Path(file.metadata['source']).name).replace(".md","")
            file.metadata['document_name'] = str(Path(file.metadata['source']).name).replace(".md",".pdf")

        logger.info(f"Loaded files successfully from {self.config.source}")
        return loaded_files
    

    def convert_into_chunks(self, files:List[Any]): 
        logger.info("Converting documents into chunks")
        # provide the splitter
        doc_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.config.chunk_size, 
            chunk_overlap=self.config.chunk_overlap,
        )

        # split the documents into chunks 
        chunks = doc_splitter.split_documents(files)
        logger.info("Chunks instantiated successfully")

        return chunks 


    def embeddings_loading(self):
        # load the embedding 
        # hugging face embedding 
        
        logger.info(f"Loading embedding: {self.config.embedding_name}")

        embedding_model = HuggingFaceEmbeddings(
            model_name=self.config.embedding_name,
            show_progress=True
        )
        
        logger.info(f"Embedding {self.config.embedding_name} loaded succesfully")
        # return the embedding to use 
        return embedding_model
    

    

    def hybrid_retriever(self, vectorStore:WeaviateVectorStore, chunks) -> EnsembleRetriever: 
        
        logger.info("Creating hybrid retriever")
        ## instantiate the semantic retriever 
        semantic_retriever = vectorStore.as_retriever(
            search_type='similarity',
            search_kwargs={"k": self.config.k}
        ) 

        ## instantiate the keyword retriever
        keyword_retriever = BM25Retriever.from_documents(
            documents=chunks,
            k=self.config.k
        )

        # hybrid approach
        hybrid_retriever_approach = EnsembleRetriever(
            retrievers=[
                semantic_retriever,
                keyword_retriever
            ],# provide the 2 retrievers to use 
            weights=[self.config.weights[0], self.config.weights[1]] # Percentage of importance for both retrievers
        )

        logger.info("Retriever Created succesfully")

        return hybrid_retriever_approach



    def reranker(self, retriever) -> ContextualCompressionRetriever:
        logger.info("Creating reranker from the retriever")
        # provide the compressor 
        flashrank_reranker = FlashrankRerank(top_n=self.config.top_n) ### TO USE THIS FIRST ADD THE LIBARY "flashrank"

        # use of reranker 
        reranked_retriever = ContextualCompressionRetriever(
            base_compressor=flashrank_reranker, # provide the reranker
            base_retriever= retriever, # provide hybrid approach retriever
        )  

        logger.info("Reranker created successfully")
        return reranked_retriever


    
    
    def start_vector_db(self, ) -> WeaviateVectorStore:
        ## instructions to start the vector DB ##

        # instantiate the client 
        weaviate_client= weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("CLUSTER_URL"), # rest endpoint (temporal cluster) get it from .env file
            auth_credentials=weaviate.classes.init.Auth.api_key(api_key=os.getenv("WEAVIATE_TEMPORAL_API_KEY")) # api key (create one first and add to .env file)
        )
        # check how many collections are there in the client 
        available_collections = [collection for collection in weaviate_client.collections.list_all()]

        # load the documents 
        documents = self.load_files()

        # convert into chunks 
        chunks = self.convert_into_chunks(files=documents)

        # load the embedding model 
        embedding_model = self.embeddings_loading()

        # create a new collection or load one depending if there are existing ones or not 
        
        if len(available_collections) == 0: 
            ## use the client to create the vector store (from the documents) 
            weaviate_vectordb = WeaviateVectorStore.from_documents(
                client=weaviate_client,
                documents=chunks,
                embedding=embedding_model
            )
        else:
            # only to connect to the vector db (without creating another collection)
            weaviate_vectordb = WeaviateVectorStore(
                client=weaviate_client,
                index_name=available_collections[0], # choose the first collection that exists
                text_key='text', # the key in weaviate
                embedding=embedding_model 
            )

        # provide the hybrid retriever 
        retriever = self.hybrid_retriever(vectorStore=weaviate_vectordb,
                                          chunks=chunks)

        # use of reranker 
        reranker_retriever = self.reranker(retriever=retriever)

        logger.info("Checking if the weaviate client is live")
        # check if the client
        if weaviate_client.is_live():
            status = "True"
            logger.info(f"It is live: Status={status}")
        else: 
            status = "False"
            logger.info(f"It is not live: Status={status}")
        
        logger.info(f"Logging status: {status} to file {self.response_file_txt}")
            ## save the status to the artifacts folder 
        with open(file=self.response_file_txt, mode='w') as saved_response: 
            saved_response.write(status)
        logger.info(f"Successfully logged the status: {status}")

        # return the weaviate vector db and the retriever
        logger.info(f"Successfully retrieved:\nVector db: {weaviate_vectordb}\n retriever:{retriever}")
        
        #weaviate_client.close() # close the connection for now 

        return weaviate_vectordb, reranker_retriever
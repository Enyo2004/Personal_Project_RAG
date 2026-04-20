### provide the entities of each phase of the pipeline ### 
from dataclasses import dataclass
from pathlib import Path
from typing import List 

### SAME CONFIG AS THE config.yaml file ### 

'''Data Ingestion Entity'''
@dataclass
class DataIngestionConfig: 
    root_dir: Path
    artifact_path: Path 
    path_name: Path


'''Data Transformation Entity'''
@dataclass
class DataTransformationConfig: 
    source: Path 
    root_dir: Path
    path_name: Path
    artifact_path: Path 
    llm: str

    
'''Vector DB Entity'''
@dataclass 
class VectorDBConfig: 
    source: Path
    path_name: Path 
    
    embedding_name: str 
    default_cluster_url: str
    llm: str
    artifact_path: Path 

    ## params ## 
    # recursive text splitter 
    chunk_size: int 
    chunk_overlap: int 

    # bm25 retriever 
    k: int

    # reranker 
    top_n: int
    
    # Ensemble retriever 
    weights: List[float]

    



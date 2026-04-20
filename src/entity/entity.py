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

    


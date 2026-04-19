### provide the entities of each phase of the pipeline ### 
from dataclasses import dataclass
from pathlib import Path

### SAME CONFIG AS THE config.yaml file ### 

'''Data Ingestion Entity'''
@dataclass
class DataIngestionConfig: 
    root_dir: Path
    artifact_path: Path 
    path_name: Path

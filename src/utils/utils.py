### IMPORTANT FUNCTIONS TO USE IN THE PROJECT ### 

# import the libraries 
import yaml 
import os 
from pathlib import Path
from box import ConfigBox

# use the logging 
from src.utils.logger_artifact import logger

# to get the right type of inputs
from ensure import ensure_annotations

'''Read yaml'''
@ensure_annotations
def read_yaml(filepath:str) -> ConfigBox:

    # pathfile 
    pathfile = Path(filepath)

    logger.info(f"Reading file {pathfile.name}")

    # read the yaml file 
    with open(pathfile, mode='r') as file: 
        # yaml file 
        yaml_file = yaml.safe_load(file)

        # provide the attribute based dict
        box_yaml_file = ConfigBox(yaml_file)
    
    # return the box yaml file 
    logger.info(f"File {pathfile.name} ready to use!")
    return box_yaml_file


'''Create directories'''
def create_directories(directories:list[Path]): 
    '''Directories'''
    for file in directories:
        logger.info(f"Creating directory {file}")
        os.makedirs(file, exist_ok=True)
        logger.info(f"Directory {file} created")


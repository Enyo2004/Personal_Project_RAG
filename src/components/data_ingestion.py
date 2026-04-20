### COMPONENTS ### 
import os 
from pathlib import Path 
import glob 
from typing import List, AnyStr

from src.entity.entity import DataIngestionConfig

from src.utils.logger_artifact import logger

'''Data Ingestion'''
class DataIngestion: 
    def __init__(self,
                 config=DataIngestionConfig):
        
        self.config= config
        
    def start_data_ingestion(self) -> List[AnyStr]:
        # provide the istructions to read the files 

        ## Load the files 
        text_files = glob.glob(
        pathname=self.config.path_name,
        root_dir=self.config.root_dir,
        )

        ## sort the files 
        text_files.sort()

        ## provide the folder path 
        folder_path = Path(os.path.join(self.config.artifact_path, self.config.root_dir))

        if folder_path.exists():
            logger.info(f"Folder already exists in {folder_path}")

        else: 
            logger.info(f"Creating folder at: {folder_path}")

        ## MAKE THE ARTIFACTS 
        for file in text_files: 
            
            # create the full path 
            full_path = Path(os.path.join(folder_path, file))

            logger.info(f"Creating file in {full_path}")

            # create the directory 
            os.makedirs(full_path.parent, exist_ok=True)

            # create the file within the directory 
            full_path.touch() 

            logger.info(f"File created in {full_path}")

            '''RAG_TXT FOLDER'''
            ## READ FROM THE LOADED DATA
            file_read = os.path.join(self.config.root_dir, file)
            with open(file=file_read, mode='r') as read_txt_file:
                read_file = read_txt_file.read()
                logger.info(f"File: {file_read} read")
                
            '''ARTIFACTS FOLDER'''
            ## WRITE IN THE ARTIFACTS 
            with open(file=full_path, mode='w') as write_txt_file: 
                write_txt_file.write(read_file)
                logger.info(f"File: {full_path} overwritten")

        
        # return the text files 
        return text_files
        
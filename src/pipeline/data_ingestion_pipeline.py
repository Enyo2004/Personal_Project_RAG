### THE DATA INGESTION PIPELINE ### 
from src.utils.logger_artifact import logger

from src.config.configuration import ConfigurationManager

from src.components.data_ingestion import DataIngestion

class DataIngestionPipeline:
    def __init__(self):
        pass

    def initiate_data_ingestion(self):
        try: 
            # provide the pipeline 
            logger.info("Starting Data Ingestion")

            config = ConfigurationManager()

            data_ingestion_config = config.get_data_ingestion_config()

            data_ingestion = DataIngestion(data_ingestion_config)

            files = data_ingestion.start_data_ingestion()
            
            logger.info("Data Ingestion finished: Files loaded correctly")

            return files
        except Exception as e:
            raise e 
        

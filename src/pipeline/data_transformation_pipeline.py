# import the Configuration manager 
from src.config.configuration import ConfigurationManager

# import the Data Transformation component 
from src.components.data_transformation import DataTransformation

from src.utils.logger_artifact import logger

class DataTransformationPipeline:
    def __init__(self):
        pass

    def initiate_data_transformation(self):
        try:
            logger.info("Starting Data Transformation Phase")
            # run the pipeline 
            config = ConfigurationManager()

            data_transformation_config = config.get_data_transformation_config()

            data_transformation = DataTransformation(data_transformation_config)

            data_transformation.create_md_directories()
            
            data_transformation.token_info()

            # ONLY USE IF WANTED TO FORCE THE LLM TO OVERWRITE THE FILES # 
            #data_transformation.llm_rewrite()
            
            data_transformation.start_data_transformation()

            logger.info("Data Transformation Phase executed correctly: Information loaded to the .md files")            
        
        except Exception as e: 
            raise e
        

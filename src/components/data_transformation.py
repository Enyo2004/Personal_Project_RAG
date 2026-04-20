# import libraries to use 
## FILES ##
import os
import glob
from pathlib import Path

## TOKENS ##
import tiktoken
from statistics import mean

## LLM ##
from dotenv import load_dotenv
from openai import OpenAI

# import the logger 
from src.utils.logger_artifact import logger

# import the config entity 
from src.entity.entity import DataTransformationConfig

"""Data Transformation Component"""
class DataTransformation: 
    def __init__(self,
                 config=DataTransformationConfig):
        # load the .env file
        load_dotenv(override=True)

        self.config = config 
        self.base_url = os.getenv("CEREBRAS_BASE_URL")
        self.api_key = os.getenv("CEREBRAS_API_KEY")

        # read the files from the data ingestion phase 
        self.files = glob.glob(
        pathname=self.config.path_name.replace('md','txt'),
        root_dir=self.config.source, 
        )      

        # sort the files
        self.files.sort()


        # provide the client 
        self.client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key
        )

        # system message 
        self.SYSTEM_MESSAGE = """YOU ARE A HELPFUL MARKDOWN FORMATTER.

        You are an expert at both English and Spanish languages.

        Your task is to reformat the text given into markdown format.

        The text that are going to be given are spiritual type, so take into account this to provide the most accurate translations possible. 

        REFORMAT IN THE MOST STRUCTURED WAY POSSIBLE BY INCLUDING ALL THE INFORMATION BUT IN A CONCISE WAY (TO AVOID OVEREXTENDING THE TEXT).

        WITHOUT EXPLANATIONS OR INITIAL MESSAGES, JUST PROVIDE THE FINAL MARKDOWN IN SPANISH

        DO NOT ADD HYPERLINKS OR ANY TYPE OF URL TO ANY IMAGE, IN THAT CASE JUST BRIEFLY EXPLAIN THE STATEMENT AS IN MARKDOWN FORMAT
        """

    def create_md_directories(self): 
        # instructions to change the txt files into md with the help of an LLM 
        
        # read the files from the data ingestion phase 

        '''TEXT FILES'''
        logger.info("Reading files from data ingestion phase")

        # sort the files 
        self.files.sort()

        '''MD FILES'''
        
    
        for file in self.files: 
            
            # convert into .md directory
            pathfile = Path(file)
            
            pathfile_md = str(pathfile).replace(".txt",".md")

            md_file = Path(os.path.join(self.config.artifact_path, self.config.root_dir, pathfile_md))
            
            print(md_file, type(md_file))
            # CREATE THE DIRECTORIES 
            # make the directories 
            os.makedirs(
                name=md_file.parent,
                exist_ok=True
            )

            logger.info(f"Directory {md_file.parent} succesfully created")

            # add the file to their correspondent folder 
            md_file.touch(exist_ok=True)

            logger.info(f"File {md_file.name} succesfully added to {md_file.parent}")
            
    def token_info(self,):

        # provide the encoder
        encoder = tiktoken.encoding_for_model('gpt-4')

        encoded_numbers = []
        
        # get the length of all the texts 
        for token_file in self.files: 
            
            token_file = Path(os.path.join(self.config.source, token_file))
            
            with open(token_file, mode='r') as file: 
                txt_file = file.read()

            encoded_text = encoder.encode(txt_file)

            number_of_tokens = len(encoded_text)

            encoded_numbers.append(number_of_tokens)

            logger.info(f"File {token_file} has {number_of_tokens} tokens")


        ### AVERAGE OF TOKENS THROUGH ALL TEXTS ###
        mean_tokens = mean(encoded_numbers)

        ### HIGHEST TOKEN COUNT ### 
        encoded_numbers.sort(reverse=True)

        highest_tokens = encoded_numbers[0]

        logger.info(f"Total Tokens: {sum(encoded_numbers)} |Average tokens of files: {mean_tokens} | Highest token count: {highest_tokens}")

    def llm_rewrite(self):
        """Write in all the files """
        
        for file in self.files: 
            """MD files"""
            # convert into md files path 
            md_file = str(file).replace("txt",'md')

            # provide the full path to read each file
            full_path = Path(os.path.join(self.config.artifact_path, self.config.root_dir, md_file))
            
            """TXT FILES"""
            # read the files 
            with open(Path(os.path.join(self.config.source, file))) as file_to_read: 
                readed_file = file_to_read.read()
                
            logger.info(f"LLM REWRITING TEXT FOR: {md_file}")
            ### LLM FUNCTIONALITY ### 
            response = self.client.chat.completions.create(
                    model=self.config.llm,
                    messages=[
                        {"role":"system", "content": self.SYSTEM_MESSAGE},
                        {"role":"user", "content": f"Proporcionar el siguiente .txt en .md (idioma español): {readed_file}"}
                    ],
                    temperature=0.7
                )

            llm_text = response.choices[0].message.content 
            logger.info(f"LLM SUCCESSFULLY CREATED TEXT FOR: {md_file}")
                
            """WRITE IN MD FILES"""
            # write in each file the text 
            with open(full_path, mode='w') as file_to_write: 
                    logger.info(f"Writing in file: {full_path.name}")
                    file_to_write.write(llm_text)
                    logger.info(f"Successfully overwriten file: {full_path.name}")
            


    def start_data_transformation(self):
        """Write in all the files """
        
        for file in self.files: 
            """MD files"""
            # convert into md files path 
            md_file = str(file).replace("txt",'md')

            # provide the full path to read each file
            full_path = Path(os.path.join(self.config.artifact_path, self.config.root_dir, md_file))
            
            with open(os.path.join(full_path), mode='r') as checking_file: 
                check_file = checking_file.read()

            # if the path has text in it do not rewrite anything 
            if check_file == "":
                logger.info(f"{os.path.join(full_path)} is empty")

                """TXT FILES"""
                # read the files 
                with open(Path(os.path.join(self.config.source, file))) as file_to_read: 
                    readed_file = file_to_read.read()
                

                logger.info(f"LLM REWRITING TEXT FOR: {md_file}")
                ### LLM FUNCTIONALITY ### 
                response = self.client.chat.completions.create(
                    model=self.config.llm,
                    messages=[
                        {"role":"system", "content": self.SYSTEM_MESSAGE},
                        {"role":"user", "content": f"Proporcionar el siguiente .txt en .md (idioma español): {readed_file}"}
                    ],
                    temperature=0.7
                )


                llm_text = response.choices[0].message.content 
                logger.info(f"LLM SUCCESSFULLY CREATED TEXT FOR: {md_file}")
                

                """WRITE IN MD FILES"""
                # write in each file the text 
                with open(full_path, mode='w') as file_to_write: 
                    logger.info(f"Writing in file: {full_path.name}")
                    file_to_write.write(llm_text)
                    logger.info(f"Successfully overwriten file: {full_path.name}")


            else: 
                logger.info(f"{os.path.join(full_path)} has words in the file: LLM will not rewrite anything")



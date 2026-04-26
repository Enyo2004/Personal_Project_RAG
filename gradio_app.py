"""GRADIO APP"""
from app import CompletePipeline
import gradio as gr

from src.utils.logger_artifact import logger

import os
from dotenv import load_dotenv

load_dotenv(override=True)

# instantiate the pipeline object
pipeline = CompletePipeline()

# provide the full workflow
response_pipeline = pipeline.workflow()
from dotenv import load_dotenv

load_dotenv(override=True)



# provide a function to use in gradio with the pipeline methods # 
def llmResponse(user_message:str, history):
    """Provide a function without the self for it to work"""
    
    # return the answeer with the initiate llm response method
    llm_response = response_pipeline.initiate_llm_response(query=user_message)

    # return the reponse
    return llm_response
    

### THE APP CONFIGURATIONS ### 
## gradio layout 

gradio_app = gr.ChatInterface(
    fn=llmResponse,
    chatbot=gr.Chatbot(
        height=1000,
        buttons=['copy'],
        layout='bubble',
        label=f"{os.getenv("PERSON_NAME")}"
    ),
    stop_btn=True,
    flagging_mode='never',
    title="Asistente Chakras",
    show_progress='minimal',
    editable=True,

    
)



if __name__ == "__main__":
    # start the weaviate connection 
    gradio_app.launch(
    inbrowser=True,
    css="footer {display: none !important}",
    footer_links=None,
    server_port=7100,
    theme=gr.themes.Neon(),
)
    

## END CONNECTIONS

# gradio connection
gr.close_all()
logger.info("Gradio ports closed successfully")


# vector db connection 
import weaviate
import os 
# instantiate the client 
logger.info("Loading Weaviate Client")

weaviate_client= weaviate.connect_to_weaviate_cloud(
            cluster_url=os.getenv("CLUSTER_URL"), # rest endpoint (temporal cluster) get it from .env file
            auth_credentials=weaviate.classes.init.Auth.api_key(api_key=os.getenv("WEAVIATE_TEMPORAL_API_KEY")) # api key (create one first and add to .env file)
        )
logger.info("Weaviate client loaded successfully")


weaviate_client.close()
logger.info("Weaviate Client closed successfully")
logger.info(f"Weaviate Client Connected: {weaviate_client.is_connected()}")

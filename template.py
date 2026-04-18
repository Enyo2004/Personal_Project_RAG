## PROVIDE THE TEMPLATE FOR THE PROJECT 

import os 
from pathlib import Path 

# project name
#project_name = "Chakras_RAG"

list_files = [
    ## YAML FILES ## 
    "config/config.yaml",
    "params.yaml",
    "schema.yaml",

    ## SRC FILES ##
    # entity (config)
    "src/entity/entity.py",
    "src/entity/__init__.py",

    # configuration manager
    "src/config/configuration.py",
    "src/config/__init__.py",

    # components 
    "src/components/__init__.py",

    # utils 
    "src/utils/utils.py",
    "src/utils/__init__.py", 
    "src/utils/logger_artifact.py",


    # pipeline 
    "src/pipeline/__init__.py",

    ## main folder ## 
    "app.py",

    ## logs 
    "logs/",

    ## artifacts 
    "artifacts/",
]


### CREATE THE FOLDER STRUCTURE WITH THE LIST OF FILES TEMPLATE 
for file in list_files: 
    print(file)

    # convert into a path file 
    pathfile = Path(file)

    # get the last subdirectorie's name from the pathfile 
    pathfile_name = pathfile.name

    if "." in pathfile_name:
        print(f"File {pathfile_name} in path: {pathfile}\n")

        # first create the directory 
        os.makedirs(pathfile.parent, exist_ok=True)

        # then create the file within the directory
        pathfile.touch(exist_ok=True)

    else: 
        print(f"Directory in: {pathfile}\n")

        # just create the directory 
        os.makedirs(pathfile, exist_ok=True)







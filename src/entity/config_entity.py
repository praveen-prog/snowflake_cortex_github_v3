import os
from src.constants import *
from src.constants.constants_github_tmp import SetUpGitHubClass
from dataclasses import dataclass
from datetime import datetime
from typing import ClassVar
from src.logger import logging


TIMESTAMP: str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S")

@dataclass
class SetUpConfig:
    setupgithubclass = SetUpGitHubClass()
    logging.info(f"Git hub repo is DDDD{setupgithubclass.GITHUB_REPO_LINK}")
    MODEL_NAME :  str = MODEL_NAME
    EMBEDDING_MODEL_NAME : str = EMBEDDING_MODEL_NAME
    RAG_APP_ID : str = RAG_APP_ID
    RAG_APP_VERSION : str = RAG_APP_VERSION
    REPOSITORY_LIST : ClassVar[list[str]] = REPOSITORY_LIST
    SNOWFLAKE_ACCOUNT : str = SNOWFLAKE_ACCOUNT
    CONNECTION_PARAMS : ClassVar[dict[str]] = CONNECTION_PARAMS
    GITHUB_TOKEN : str = setupgithubclass.GITHUB_TOKEN
    GITHUB_REPO_LINK : str  = setupgithubclass.GITHUB_REPO_LINK
    GITHUB_OWNER : str = setupgithubclass.GITHUB_OWNER
    GITHUB_REPO_NAME: str = setupgithubclass.GITHUB_REPO_NAME
    GITHUB_REPO_BRANCH : str = setupgithubclass.GITHUB_REPO_BRANCH
    GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = setupgithubclass.GITHUB_FILTER_DIRECTORIES
    GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = setupgithubclass.GITHUB_FILTER_EXTENSIONS
    

    

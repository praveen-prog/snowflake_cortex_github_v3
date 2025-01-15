import os
from datetime import date
from dotenv import load_dotenv
from src.exception import snowflakecortexerror
from typing import ClassVar
load_dotenv()


MODEL_NAME : str = "mistral-large2"
EMBEDDING_MODEL_NAME : str = "Snowflake/snowflake-arctic-embed-m"
RAG_APP_ID : str = "RAG Chatbot App v5"
RAG_APP_VERSION : str = "1.0"
REPOSITORY_LIST : ClassVar[list[str]] = [
        "github.com/user/repo1",
        "github.com/user/repo2",
        "github.com/user/repo3",
        "github.com/user/repo4",
        "https://api.github.com/repos/praveen-prog/docs/branches/main",
        "https://api.github.com/repos/praveen-prog/reltiosqlchatbot/branches/main",
        "https://api.github.com/repos/praveen-prog/prisma-cloud-devsecops-workshop/branches/main"
    ]
#os.chdir("../../")
SNOWFLAKE_ACCOUNT : str =   os.environ.get("SNOWFLAKE_ACCOUNT")
CONNECTION_PARAMS : ClassVar[dict[str]] = {
  "account":  os.environ.get("SNOWFLAKE_ACCOUNT"),
  "user": os.environ.get("SNOWFLAKE_USER"),
  "password": os.environ.get("SNOWFLAKE_USER_PASSWORD"),
  "role": os.environ.get("SNOWFLAKE_ROLE"),
  "database": os.environ.get("SNOWFLAKE_DATABASE"),
  "schema": os.environ.get("SNOWFLAKE_SCHEMA"),
  "warehouse": os.environ.get("SNOWFLAKE_WAREHOUSE")
}
GITHUB_TOKEN : str = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO_LINK : str = "https://api.github.com/repos/praveen-prog/docs/branches/main"
GITHUB_OWNER : str = "praveen-prog"
GITHUB_REPO_NAME: str = "docs"
GITHUB_REPO_BRANCH: str = "main"
GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = ["content"]
GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = [".md"]
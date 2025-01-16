import os
from datetime import date
from dotenv import load_dotenv
from dataclasses import dataclass
from src.exception import snowflakecortexerror
from typing import ClassVar
from src.logger import logging

load_dotenv()

@dataclass
class SetUpGitHubClass:
    GITHUB_TOKEN : str = os.environ.get("GITHUB_TOKEN")
    GITHUB_REPO_LINK : str = "https://api.github.com/repos/praveen-prog/docs/branches/main"
    GITHUB_OWNER : str = "praveen-prog"
    GITHUB_REPO_NAME: str = "docs"
    GITHUB_REPO_BRANCH: str = "main"
    GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = ["content"]
    GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = [".md", ".py"]

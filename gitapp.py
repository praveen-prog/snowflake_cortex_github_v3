import streamlit as st
import os

# Define the dropdown options
dropdown_options = [
    "github.com/user/repo1",
    "github.com/user/repo2",
    "github.com/user/repo3",
    "github.com/user/repo4",
    "https://api.github.com/repos/praveen-prog/docs/branches/main",
    "https://api.github.com/repos/praveen-prog/reltiosqlchatbot/branches/main",
    "https://api.github.com/repos/praveen-prog/prisma-cloud-devsecops-workshop/branches/main",
]

# Function to parse GitHub owner, repo name, and branch
def parse_github_url(url):
    if "https://api.github.com/repos/" in url:
        parts = url.replace("https://api.github.com/repos/", "").split("/")
        owner = parts[0]
        repo_name = parts[1]
        branch = parts[3] if len(parts) > 3 else "main"
    else:
        parts = url.split("/")
        owner = parts[1]
        repo_name = parts[2]
        branch = "main"
    return owner, repo_name, branch

# Streamlit app
st.title("GitHub Repository Selector")

# Initialize session state for the selected repository
if "selected_repo" not in st.session_state:
    st.session_state.selected_repo = dropdown_options[0]

# Dropdown for selecting a repository
selected_repo = st.selectbox(
    "Select a GitHub Repository",
    dropdown_options,
    index=dropdown_options.index(st.session_state.selected_repo)
    if st.session_state.selected_repo in dropdown_options
    else 0,
    key="selected_repo",
)

if st.button("Generate File and Start Process"):
    # Parse the selected repository
    owner, repo_name, branch = parse_github_url(st.session_state.selected_repo)

    # Generate the content for github_constants_tmp.py
    file_content = f"""import os
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
    GITHUB_REPO_LINK : str = "{st.session_state.selected_repo}"
    GITHUB_OWNER : str = "{owner}"
    GITHUB_REPO_NAME: str = "{repo_name}"
    GITHUB_REPO_BRANCH: str = "{branch}"
    GITHUB_FILTER_DIRECTORIES : ClassVar[list[str]] = ["content"]
    GITHUB_FILTER_EXTENSIONS : ClassVar[list[str]] = [".md", ".py"]
"""

    # Write the content to the file
    with open("src/constants/constants_github_tmp.py", "w") as file:
        file.write(file_content)

    st.success("File github_constants_tmp.py created successfully!")

    # Run the backend process
    os.system("streamlit run app.py")

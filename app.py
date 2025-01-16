import streamlit as st
import os
import sys
from datetime import datetime
import socket
import webbrowser
import pandas
import subprocess

# Import custom modules
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.entity.artifacts_entity import DataIngestionArtifact
from src.data_ingestion import DataIngestionClass
from src.training_pipeline import TrainingPipeline

# Set page configuration
st.set_page_config(
    page_title="Code Analysis Chatbot",
    page_icon="🤖",
    layout="centered",
)

def refresh_app():
    subprocess.Popen(["python", "sandr.py"])

# Add the refresh button at the top-right
st.sidebar.button("App Refresh", on_click=refresh_app)

@st.cache_resource
def get_training_pipeline():
    """Initialize the TrainingPipeline object and cache it to prevent multiple sessions."""
    return TrainingPipeline()

def open_dashboard():
    """Render the HTML dashboard in the current tab."""
    #st.title("Dashboard Viewer")
    st.markdown(
        """
        <style>
        .centered-content {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100%;
        }
        .dashboard-container {
            border: 2px solid #4CAF50;
            border-radius: 10px;
            padding: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
    # Main content
    st.markdown("<div class='centered-content'>", unsafe_allow_html=True)
    st.markdown(
        "<div class='dashboard-container'>"
        "<h3>Tru Lens Feedback Dashboard</h3>"
        "</div>",
        unsafe_allow_html=True,
    )
    # Rendering the HTML in the current tab
    if os.path.exists("src/templates/sample.html"):

        st.html("src/templates/sample.html")
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("Please enter the question/perform referesh")

    

def find_replace_in_file(file_path, old_string, new_string):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
        file_content = file_content.replace(old_string, new_string)
        with open(file_path, 'w') as file:
            file.write(file_content)
    except Exception as e:
            raise snowflakecortexerror(e,sys)   

def print_selected_repository(repo):
    try:
        """Print the selected repository."""
        repo_link = repo.split("/")
        selected_owner_name = repo_link[4]
        selected_repo_name = repo_link[5]
        selected_branch_name = repo_link[7]
        
        source_file = os.path.join(os.getcwd(),"src/constants/constants_github_orig.py")
        print(f"Source directory is {source_file}")
        destination_file = os.path.join(os.getcwd(),"src/constants/constants_github_tmp.py")
        subprocess.run(["cp", source_file, destination_file])
        logging.info(f"File copy completed successfully to {destination_file}")
        logging.info("Creating new Temp file Constants file for rep link")    
        old_string = "https://api.github.com/repos/praveen-prog/docs/branches/main"
        new_string = repo
        find_replace_in_file(destination_file, old_string, new_string)
        logging.info("Created new Temp file Constants file for rep link")

        logging.info("Creating new Temp file Constants file for rep owner")    
        old_string = "praveen-prog"
        new_string = selected_owner_name
        find_replace_in_file(destination_file, old_string, new_string)
        logging.info("Created new Temp file Constants file for rep owner")     

        logging.info("Creating new Temp file Constants file for repo name")    
        old_string = "docs"
        new_string = selected_repo_name
        find_replace_in_file(destination_file, old_string, new_string)
        logging.info("Created new Temp file Constants file for repo name")      

        logging.info("Creating new Temp file Constants file for branch name")    
        old_string = "main"
        new_string = selected_branch_name
        find_replace_in_file(destination_file, old_string, new_string)
        logging.info("Created new Temp file Constants file for branch name")    

        st.write(f"Owner Name: {selected_owner_name}")
        st.write(f"Repo Name: {selected_repo_name}")
        st.write(f"Branch Name: {selected_branch_name}")
        st.write(f"Repository: {repo}")
                 
    except Exception as e:
            raise snowflakecortexerror(e,sys)           

def chatbot_page():
    # Title and subheader with emoji
    st.title("🔎 Code Analysis Chatbot")
    #st.subheader("Ask me anything about your source code!")

    # Add a button for opening the Dashboard in a new tab, position it at the top right
    st.markdown(
        """
        <style>
        .css-1d391kg {
            display: flex;
            justify-content: flex-end;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("TruLens Dashboard"):
        open_dashboard()

    # CSS for styling chat bubbles and timestamps
    st.markdown(
        """
        <style>
        .user-bubble {
            background-color: #DCF8C6;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 6px;
            max-width: 75%;
            text-align: left;
        }
        .bot-bubble {
            background-color: #E4E6EB;
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 6px;
            max-width: 75%;
            text-align: left;
        }
        .chat-container {
            display: flex;
            flex-direction: column;
        }
        .user-row {
            justify-content: flex-end;
            display: flex;
        }
        .bot-row {
            justify-content: flex-start;
            display: flex;
        }
        .timestamp {
            font-size: 0.8rem;
            color: gray;
            margin-top: -5px;
            margin-bottom: 10px;
        }
        img.chat-icon {
            width: 35px;
            height: 35px;
            margin-right: 12px;
            border-radius: 50%;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Initialize session state to store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    st.subheader("Ask me anything about your source code!")
    # Chat interface: Display conversation history
    with st.container(height=300):
        for msg in st.session_state.messages:
            timestamp = msg.get("timestamp", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if msg["role"] == "user":
                st.markdown(
                    f"""
                    <div class="chat-container">
                        <div class="user-row">
                            <div>
                                <div class="user-bubble">{msg['content']}</div>
                                <div class="timestamp">{timestamp}</div>
                            </div>
                            <img class="chat-icon" src="https://img.icons8.com/color/48/user.png"/>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            elif msg["role"] == "bot":
                st.markdown(
                    f"""
                    <div class="chat-container">
                        <div class="bot-row">
                            <img class="chat-icon" src="https://img.icons8.com/color/48/robot.png"/>
                            <div>
                                <div class="bot-bubble">{msg['content']}</div>
                                <div class="timestamp">{timestamp}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # Checkbox to toggle the `run_only_search_retriever` value
    run_only_search_retriever = st.checkbox("Run only search retriever", value=True)

    # Input field for the user's query
    query = st.text_input("Your query:", placeholder="Type your question here...")

    # Execute on query submission
    if st.button("Send"):
        if query.strip():  # Ensure query is not empty
            st.session_state.messages.append({"role": "user", "content": query, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

            obj = get_training_pipeline()  # Get the cached TrainingPipeline instance
            try:
                if run_only_search_retriever:
                    st.write("Analyzing the code...")
                    result = obj.run_pipeline(query=query, run_only_search_retriever=run_only_search_retriever)
                    st.success("Answer retrieved successfully!")
                    st.session_state.messages.append({"role": "bot", "content": result, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    st.rerun()

                else:
                    st.write("Pipeline execution in progress... Please wait.")
                    result = obj.run_pipeline(query=query, run_only_search_retriever=run_only_search_retriever)
                    st.success("Pipeline refreshed successfully!")
                    st.session_state.messages.append({"role": "bot", "content": result, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                    st.rerun()
            except Exception as e:
                error_msg = f"An error occurred: {str(e)}"
                st.session_state.messages.append({"role": "bot", "content": error_msg, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})
                st.rerun()

def main():
    try: 
        setupconfig = SetUpConfig()
        repository_list = setupconfig.REPOSITORY_LIST
        
        sample_repositories = repository_list

        if "show_chatbot" not in st.session_state:
            st.session_state.show_chatbot = False
        
        if "repository_confirmed" not in st.session_state:
            st.session_state.repository_confirmed = False    



        if not st.session_state.show_chatbot:
            # Apply custom style with HTML and CSS
            st.markdown(
                """
                <style>
                .custom-container {
                    background-color: #f9f9f9;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
                    border: 1px solid #e1e1e1;
                }
                .custom-title {
                    font-family: 'Arial', sans-serif;
                    font-size: 24px;
                    font-weight: bold;
                    color: #4a90e2;
                    margin-bottom: 10px;
                }
                .custom-text {
                    font-family: 'Arial', sans-serif;
                    font-size: 16px;
                    color: #333;
                    line-height: 1.5;
                }
                </style>
                """,
                unsafe_allow_html=True,
            )

            # Create a custom container
            container = st.container(border=True)  
            container.markdown('<h2 class="custom-title">Welcome to the Source Code Analysis Chatbot</h2>', unsafe_allow_html=True)  
            st.write("Explore insights and ask questions about your source code.")

            selected_repo = st.selectbox("Select a Sample Repository:",sample_repositories,index=None, placeholder="Select a repository" , key="repo_selector")

            if st.button("Confirm Repository"):
                if selected_repo:  # Ensure a repository is selected
                    st.session_state.repository_confirmed = True
                    logging.info(f"Selected repository is {selected_repo}")
                    print_selected_repository(selected_repo)
                    #st.success(f"Selected repository is {selected_repo}")

            if st.button("Proceed"):
                if st.session_state.repository_confirmed:
                    subprocess.run(["rm","src/templates/sample.html"])
                    st.session_state.show_chatbot = True
                    st.rerun()
                else:
                    st.warning("Please confirm the repository before proceeding.")
        else:
            chatbot_page()
    except Exception as e:
            raise snowflakecortexerror(e,sys)          

if __name__ == "__main__":
    main()

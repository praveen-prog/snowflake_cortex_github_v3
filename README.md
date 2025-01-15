
1.Connect to the account snowsql -a account-locator -u username
Execute below statements onetime.

ALTER ACCOUNT SET CORTEX_ENABLED_CROSS_REGION = 'AWS_US';
USE ROLE ACCOUNTADMIN;

CREATE OR REPLACE WAREHOUSE LLMOPS_WH_M WAREHOUSE_SIZE=MEDIUM;
CREATE OR REPLACE DATABASE LLMOPS_DB;
CREATE OR REPLACE SCHEMA LLMOPS_SCHEMA;

USE LLMOPS_DB.LLMOPS_SCHEMA;

2.Configure the .env file
# Loading data from github
GITHUB_TOKEN=<your github token>

# Snowflake details
SNOWFLAKE_USER=<your user name>
SNOWFLAKE_USER_PASSWORD=<your password>
SNOWFLAKE_ACCOUNT=<your snowflake account>
SNOWFLAKE_DATABASE=<your database>
SNOWFLAKE_SCHEMA=<your schema>
SNOWFLAKE_WAREHOUSE=<your warehouse>
SNOWFLAKE_ROLE=<snowflake role>
SNOWFLAKE_CORTEX_SEARCH_SERVICE=<your cortex search service name to be created>


3.Run the streamlit app with below command
streamlit run app.py


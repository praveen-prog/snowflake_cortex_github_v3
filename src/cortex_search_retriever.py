import os
import sys
import pandas 
from dotenv import load_dotenv
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.prompt import *
#from src.entity.artifacts_entity import  DataProcessingArtifact
from snowflake.core import Root
from typing import List
from snowflake.cortex import Complete
from trulens.apps.custom import instrument
   
from trulens.core import TruSession
from trulens.connectors.snowflake import SnowflakeConnector
from trulens.providers.cortex.provider import Cortex
from trulens.core import Feedback
from trulens.core import Select
import numpy as np
from trulens_eval.guardrails.base import context_filter
from trulens_eval import TruCustomApp,TruChain, Huggingface, Tru




load_dotenv()
tru = Tru()
#tru.reset_database()

class CortexSearchRetriever:

    def __init__(self,session, limit_to_retrieve: int = 4):
        try:
            self.snowpark_session = session
            self.limit_to_retrieve = limit_to_retrieve
        except Exception as e:
            raise snowflakecortexerror(e,sys) 
    def context_relevance_score(self ) -> str:
        try:
            self.snowpark_session 
            setupconfig = SetUpConfig()
            self.model_name = setupconfig.MODEL_NAME
            provider = Cortex(self.snowpark_session , self.model_name )

            # note: feedback function used for guardrail must only return a score, not also reasons
            f_context_relevance_score = (
                Feedback(provider.context_relevance, name = "Context Relevance")
                .on_input()
                .on(Select.RecordCalls.retrieve.rets)
                )
            return f_context_relevance_score
        
        except Exception as e:
            raise snowflakecortexerror(e,sys)              

    def retrieve(self, query: str) -> List[str]:
        try:
            logging.info("Entered the retrieve method of CortexSearchRetriever")
            #self.connection_params = self.setupconfig.CONNECTION_PARAMS
            snowpark_session = self.snowpark_session
            logging.info(f"Type of snowpark session is {type(snowpark_session)}")
            root = Root(self.snowpark_session)
            cortex_search_service = (
            root
            .databases[os.environ.get("SNOWFLAKE_DATABASE")]
            .schemas[os.environ.get("SNOWFLAKE_SCHEMA")]
            .cortex_search_services[os.environ["SNOWFLAKE_CORTEX_SEARCH_SERVICE"]]
        )
            resp = cortex_search_service.search(
                    query=query,
                    columns=["doc_text"],
                    limit=self.limit_to_retrieve,
                )
            logging.info("Exited the retrieve method of CortexSearchRetriever")
            
            if resp.results:
                return [curr["doc_text"] for curr in resp.results]
            else:
                return []
            
        except Exception as e:
            raise snowflakecortexerror(e,sys)             

    @instrument
    def retrieve_context(self, query: str) -> list:
        """
        Retrieve relevant text from vector store.

        """
        @context_filter(lambda: self.context_relevance_score(), 0.50, keyword_for_prompt="query")
        def inner_retrieve_context(query):
            return self.retrieve(query)
        return self.retrieve(query)

    @instrument
    def generate_completion(self, query: str, context_str: list) -> str:
        """
        Generate answer from context.
        """
        setupconfig = SetUpConfig()
        self.model_name = setupconfig.MODEL_NAME
        prompt = f"""
          {chatbot_system_prompt}
          Context: {context_str}
          Question:
          {query}
          Answer:
        """
        return Complete(self.model_name , prompt)

    @instrument
    def query(self, query: str) -> str:
        context_str = self.retrieve_context(query)
        return self.generate_completion(query, context_str)      
 

    def tru_lens_integ(self,query):
        try:
            rag = CortexSearchRetriever(session=self.snowpark_session)

            prompts = [query]
            logging.info(f"List value is DDDDD  :{prompts} ")
            logging.info("Creating trulens session")
            setupconfig = SetUpConfig()
            self.model_name = setupconfig.MODEL_NAME
            snowpark_session = self.snowpark_session
            self.rag_app_id = setupconfig.RAG_APP_ID
            self.rag_app_version = setupconfig.RAG_APP_VERSION
            tru_snowflake_connector = SnowflakeConnector(snowpark_session=snowpark_session)
            tru_session = TruSession(connector=tru_snowflake_connector)
            logging.info("tru session created successfully")

            #provider = Cortex(snowpark_session.connection, "llama3.1-8b")
            provider = Cortex(snowpark_session, self.model_name )

            f_groundedness = (
                Feedback(
                provider.groundedness_measure_with_cot_reasons, name="Groundedness")
                .on(Select.RecordCalls.retrieve_context.rets[:].collect())
                .on_output()
            )

            f_context_relevance = (
                Feedback(
                provider.context_relevance,
                name="Context Relevance")
                .on_input()
                .on(Select.RecordCalls.retrieve_context.rets[:])
                .aggregate(np.mean)
            )

            f_answer_relevance = (
                Feedback(
                provider.relevance,
                name="Answer Relevance")
                .on_input()
                .on_output()
                .aggregate(np.mean)
            )

            feedbacks = [f_context_relevance,
                        f_answer_relevance,
                        f_groundedness,
                    ]        
                
            tru_rag = TruCustomApp(rag,
                app_id = self.rag_app_id ,
                app_version = self.rag_app_version,
                feedbacks = [f_groundedness, f_answer_relevance, f_context_relevance])  
             
            with tru_rag as recording:
                for prompt in prompts:
                    result = rag.query(prompt)
                    print(result)
            print(f" Leadeboard is  : {tru_session.get_leaderboard()}")

            df = tru_session.get_leaderboard()
            # Generate the HTML table
            html_table = df.to_html(
                classes='table table-striped table-bordered table-hover',
                header=True,
                justify='center',
                border=0
            )

            # Add the enhanced HTML structure
            html_document = f"""
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
                <title>Leaderboard</title>
            </head>
            <body>
                <div class="container mt-5">
                    <h3 class="text-center">Summary</h3>
                    <div class="table-responsive">
                        {html_table}
                    </div>
                </div>
            </body>
            </html>
            """

        
            with open("src/templates/sample.html","w") as f:
                f.write((html_document))
            
            #tru_session.reset_database()   
            #tru_session.run_dashboard(port=8502)   
                 
            return result
        except Exception as e:
            raise snowflakecortexerror(e,sys)       

    #tru.run_dashboard(port=8502)         
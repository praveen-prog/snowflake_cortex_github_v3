import os
import sys
from src.logger import logging
from src.exception import snowflakecortexerror
from src.entity.config_entity import SetUpConfig
from src.entity.artifacts_entity import DataIngestionArtifact , DataProcessingArtifact
from src.data_ingestion import DataIngestionClass
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.core.ingestion import IngestionPipeline

class DataProcessingClass:
    def __init__(self,data_ingestion_artifact : DataIngestionArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise snowflakecortexerror(e,sys)      

    def semantic_splitting(self,setupconfig : SetUpConfig = SetUpConfig()) ->  DataProcessingArtifact:
        try:
            self.setupconfig = setupconfig
            data_ingestion_artifact = self.data_ingestion_artifact 
            self.embedding_model_name = setupconfig.EMBEDDING_MODEL_NAME
            logging.info(f"Emebedding model used is {self.embedding_model_name}")   
            #logging.info(f"Data ingestion artifact is BBBBB: {data_ingestion_artifact}")    
            embed_model = HuggingFaceEmbedding(self.embedding_model_name)

            splitter = SemanticSplitterNodeParser(
            buffer_size=1, breakpoint_percentile_threshold=85, embed_model=embed_model
             )
            logging.info(f"splitter value is : {splitter}")
            clean_up_document_path = data_ingestion_artifact
            #logging.info(f"Clean up document is {clean_up_document_path}")
            cortex_search_pipeline = IngestionPipeline(transformations=[splitter,],)
            results = cortex_search_pipeline.run(show_progress=True,documents=clean_up_document_path)
            return results
            
        except Exception as e:
            raise snowflakecortexerror(e,sys)      
#obj = DataProcessingClass()
#obj.semantic_splitting()
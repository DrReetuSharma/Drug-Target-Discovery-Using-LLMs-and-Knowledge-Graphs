import json
from typing import Optional, List
from langchain.schema import Document
import neo4j_utils as nu
from .prompts import BioCypherPromptEngine

class DatabaseAgent:
    def __init__(
        self,
        model_name: str,
        connection_args: dict,
        schema_config_or_info_dict: dict,
        conversation_factory: Optional[callable] = None,
    ) -> None:
        """
        Create a DatabaseAgent that interacts with a Neo4j database using a prompt engine.

        Args:
            model_name (str): The name of the model.
            connection_args (dict): Connection arguments for the database (db_name, host, port, user, password).
            schema_config_or_info_dict (dict): Schema information for the database.
            conversation_factory (callable, optional): Function to create a conversation for KG queries.
        """
        self.model_name = model_name
        self.connection_args = connection_args
        self.schema_config_or_info_dict = schema_config_or_info_dict
        self.conversation_factory = conversation_factory
        self.prompt_engine = BioCypherPromptEngine(
            model_name=model_name,
            schema_config_or_info_dict=schema_config_or_info_dict,
            conversation_factory=conversation_factory,
        )
        self.driver = None

    def connect(self) -> None:
        """
        Connect to the Neo4j database.
        """
        db_name = self.connection_args.get("db_name", "neo4j")
        uri = f"bolt://{self.connection_args.get('host')}:{self.connection_args.get('port')}"
        user = self.connection_args.get("user")
        password = self.connection_args.get("password")
        self.driver = nu.Driver(db_name=db_name, db_uri=uri, user=user, password=password)

    def is_connected(self) -> bool:
        """
        Check if connected to the database.
        """
        return self.driver is not None

    def get_query_results(self, query: str, k: int = 3) -> List[Document]:
        """
        Generate a query using the prompt engine and return the results.

        Args:
            query (str): The query string.
            k (int): Number of results to return.

        Returns:
            List[Document]: List of Document objects containing query results.
        """
        cypher_query = self.prompt_engine.generate_query(query)
        results = self.driver.query(query=cypher_query)

        documents = []
        for result in results[0][:k]:
            documents.append(Document(
                page_content=json.dumps(result),
                metadata={"cypher_query": cypher_query},
            ))

        return documents

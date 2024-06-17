from typing import Optional, List, Tuple, Any
from .database_agent import DatabaseAgent
from .vectorstore_agent import VectorDatabaseAgentMilvus


class RagAgentModeEnum:
    VectorStore = "vectorstore"
    KG = "kg"


class RagAgent:
    def __init__(
        self,
        mode: str,
        model_name: str,
        connection_args: dict,
        n_results: Optional[int] = 3,
        use_prompt: Optional[bool] = False,
        schema_config_or_info_dict: Optional[dict] = None,
        conversation_factory: Optional[callable] = None,
        embedding_func: Optional[object] = None,
        documentids_workspace: Optional[List[str]] = None,
    ) -> None:
        """
        Create a RAG agent that can return results from a database or vector
        store using a query engine.

        Args:
            mode (str): The mode of the agent. Either "kg" or "vectorstore".

            model_name (str): The name of the model to use.

            connection_args (dict): A dictionary of arguments to connect to the
                database or vector store. Contains database name (in case of
                multiple DBs in one DBMS), host, port, user, and password.

            n_results: the number of results to return for method
                generate_response

            use_prompt (bool): Whether to use the prompt for the query. If
                False, will not retrieve any results and return an empty list.

            schema_config_or_info_dict (dict): A dictionary of schema
                information for the database. Required if mode is "kg".

            conversation_factory (callable): A function used to create a
                conversation for creating the KG query. Required if mode is
                "kg".

            embedding_func (object): An embedding function. Required if mode is
                "vectorstore".

            documentids_workspace (Optional[List[str]], optional): a list of
                document IDs that defines the scope within which similarity
                search occurs. Defaults to None, which means the operations will
                be performed across all documents in the database.

        Raises:
            ValueError: If an invalid mode is provided or required arguments
                are missing.
        """
        if mode not in [RagAgentModeEnum.KG, RagAgentModeEnum.VectorStore]:
            raise ValueError("Invalid mode. Choose either 'kg' or 'vectorstore'.")

        if mode == RagAgentModeEnum.KG and not schema_config_or_info_dict:
            raise ValueError("Please provide a schema config or info dict.")

        if mode == RagAgentModeEnum.VectorStore and not embedding_func:
            raise ValueError("Please provide an embedding function.")

        self.mode = mode
        self.model_name = model_name
        self.connection_args = connection_args
        self.n_results = n_results
        self.use_prompt = use_prompt
        self.schema_config_or_info_dict = schema_config_or_info_dict
        self.conversation_factory = conversation_factory
        self.embedding_func = embedding_func
        self.documentids_workspace = documentids_workspace
        self.last_response = []
        self.agent = None
        self.query_func = None
        self._initialize_agent()

    def _initialize_agent(self) -> None:
        """Initialize the appropriate database or vector store agent."""
        if self.mode == RagAgentModeEnum.KG:
            self.agent = DatabaseAgent(
                model_name=self.model_name,
                connection_args=self.connection_args,
                schema_config_or_info_dict=self.schema_config_or_info_dict,
                conversation_factory=self.conversation_factory,
            )
            self.query_func = self.agent.get_query_results
        elif self.mode == RagAgentModeEnum.VectorStore:
            self.agent = VectorDatabaseAgentMilvus(
                embedding_func=self.embedding_func,
                connection_args=self.connection_args,
            )
            self.query_func = self.agent.similarity_search

        if self.agent:
            self.agent.connect()

    def generate_responses(self, user_question: str) -> List[Tuple[str, Any]]:
        """
        Run the query function according to the mode and return the results in a
        uniform format (list of tuples, where the first element is the text for
        RAG and the second element is the metadata).

        Args:
            user_question (str): The user question.

        Returns:
            results (List[Tuple[str, Any]]): A list of tuples containing the results.
        """
        if not self.use_prompt:
            return []

        if not self.query_func:
            raise ValueError("Agent not initialized.")

        results = self.query_func(user_question, self.n_results)

        self.last_response = [
            (result.page_content, result.metadata) for result in results
        ]

        return self.last_response

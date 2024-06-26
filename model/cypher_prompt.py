from typing import Optional
import os
import json
import yaml
from ._miscellaneous import verify_iterable, sentencecase_to_pascalcase
from .llms_connection import ChatInterface, GptChat


class CypherPrompt:
    def __init__(
        self,
        schema_file_path: Optional[str] = None,
        schema_config_or_info_dict: Optional[dict] = None,
        model_name: str = "gpt-3.5-turbo",
        chat_factory: Optional[callable] = None,
    ) -> None:
        """
        CypherPrompt class for generating queries from schema configurations.

        Args:

             Model_name: Deprecated. Model name for the chat.
             
            schema_file_path: Path to a biocypher schema configuration
                file or schema information output.

            schema_config_or_info_dict: Dictionary containing schema configuration
                or schema information.

            chat_factory: Function to create a chat for KG query.
        """
        if not schema_file_path and not schema_config_or_info_dict:
            raise ValueError(
                "Please provide the schema configuration or schema info as a "
                "path to a file or as a dictionary."
            )

        if schema_file_path and schema_config_or_info_dict:
            raise ValueError(
                "Please provide the schema configuration or schema info as a "
                "path to a file or as a dictionary, not both."
            )

        self.chat_factory = (
            chat_factory
            if chat_factory is not None
            else self._get_chat
        )

        if schema_file_path:
            with open(schema_file_path, "r") as f:
                schema_config = yaml.safe_load(f)
        elif schema_config_or_info_dict:
            schema_config = schema_config_or_info_dict

        is_schema_info = schema_config.get("is_schema_info", False)

        self.entities = {}
        self.relationships = {}

        if not is_schema_info:
            for key, value in schema_config.items():
                name_indicates_relationship = (
                    "interaction" in key.lower() or "association" in key.lower()
                )
                if "represented_as" in value:
                    if (
                        value["represented_as"] == "node"
                        and not name_indicates_relationship
                    ):
                        self.entities[sentencecase_to_pascalcase(key)] = value
                    elif (
                        value["represented_as"] == "node"
                        and name_indicates_relationship
                    ):
                        self.relationships[
                            sentencecase_to_pascalcase(key)
                        ] = value
                    elif value["represented_as"] == "edge":
                        self.relationships[
                            sentencecase_to_pascalcase(key)
                        ] = value
        else:
            for key, value in schema_config.items():
                if not isinstance(value, dict):
                    continue
                if value.get("present_in_knowledge_graph", None) == False:
                    continue
                if value.get("is_relationship", None) == False:
                    self.entities[sentencecase_to_pascalcase(key)] = value
                elif value.get("is_relationship", None) == True:
                    value = self._capitalise_source_and_target(value)
                    self.relationships[sentencecase_to_pascalcase(key)] = value

        self.question = ""
        self.selected_entities = []
        self.selected_relationships = []
        self.selected_relationship_labels = {}
        self.rel_directions = {}
        self.model_name = model_name

    def _capitalise_source_and_target(self, relationship: dict) -> dict:
        """
        Capitalizes sources and targets to match entity names.

        Args:
            relationship: Dictionary with source and target information.

        Returns:
            Dictionary with capitalized sources and targets.
        """
        if "source" in relationship:
            if isinstance(relationship["source"], str):
                relationship["source"] = sentencecase_to_pascalcase(
                    relationship["source"]
                )
            elif isinstance(relationship["source"], list):
                relationship["source"] = [
                    sentencecase_to_pascalcase(s)
                    for s in relationship["source"]
                ]
        if "target" in relationship:
            if isinstance(relationship["target"], str):
                relationship["target"] = sentencecase_to_pascalcase(
                    relationship["target"]
                )
            elif isinstance(relationship["target"], list):
                relationship["target"] = [
                    sentencecase_to_pascalcase(t)
                    for t in relationship["target"]
                ]
        return relationship

    def generate_query(
        self, question: str, query_language: Optional[str] = "Cypher"
    ) -> str:
        """
        Generates a database query based on user's question.

        Args:
            question: User's question.

            query_language: Query language (default is Cypher).

        Returns:
            Generated database query.
        """
        success1 = self._select_entities(
            question=question, chat=self.chat_factory()
        )
        if not success1:
            raise ValueError(
                "Entity selection failed. Please try again with a different "
                "question."
            )
        success2 = self._select_relationships(
            chat=self.chat_factory()
        )
        if not success2:
            raise ValueError(
                "Relationship selection failed. Please try again with a "
                "different question."
            )
        success3 = self._select_properties(
            chat=self.chat_factory()
        )
        if not success3:
            raise ValueError(
                "Property selection failed. Please try again with a different "
                "question."
            )

        return self._generate_query(
            question=question,
            entities=self.selected_entities,
            relationships=self.selected_relationship_labels,
            properties=self.selected_properties,
            query_language=query_language,
            chat=self.chat_factory(),
        )

    def _get_chat(
        self, model_name: Optional[str] = None
    ) -> "ChatInterface":
        """
        Creates a chat object for knowledge graph query.

        Args:
            model_name: Model name for the conversation.

        Returns:
            chat object.
        """
        conversation = GptChat(
            model_name=model_name or self.model_name,
            prompts={},
            correct=False,
        )
        chat.set_api_key(
            api_key=os.getenv("OPENAI_API_KEY"), user="test_user"
        )
        return chat

    def _select_entities(
        self, question: str, conversation: "Conversation"
    ) -> bool:
        """
        Selects relevant entities based on user's question.

        Args:
            question: User's question.

            conversation: Conversation object.

        Returns:
            True if at least one entity was selected, False otherwise.
        """
        self.question = question

        chat.append_system_message(
            (
                "You have access to a knowledge graph that contains "
                f"these entity types: {', '.join(self.entities)}. Your task is "
                "to select the entity types that are relevant to the user's question "
                "for subsequent use in a query. Only return the entity types, "
                "comma-separated, without any additional text. Do not return "
                "entity names, relationships, or properties."
            )
        )

        msg, token_usage, correction = chat.query(question)

        result = msg.split(",") if msg else []

        if result:
            for entity in result:
                entity = entity.strip()
                if entity in self.entities:
                    self.selected_entities.append(entity)

        return bool(result)

    def _select_relationships(self, conversation: "ChatInterface") -> bool:
        """
        Selects relevant relationships based on selected entities.

        Args:
            chat: chat object.

        Returns:
            True if at least one relationship was selected, False otherwise.
        """
        if not self.question:
            raise ValueError(
                "No question found. Please make sure to run entity selection "
                "first."
            )

        if not self.selected_entities:
            raise ValueError(
                "No entities found. Please run the entity selection step first."
            )

        relations_dict = {}
        source_and_target_present = False
        for key, value in self.relationships.items():
            if "source" in value and "target" in value:
                source = ensure_iterable(value["source"])
                target = ensure_iterable(value["target"])
                pairs = []
                for s in source:
                    for t in target:
                        pairs.append((s, t))
                relations_dict[key] = pairs
                source_and_target_present = True
            else:
                relations_dict[key] = {}

        if source_and_target_present:
            rels_with_both = {}
            rels_with_either = {}
            for key, value in relations_dict.items():
                for pair in value:
                    if pair[0] in self.selected_entities:
                        if pair[1] in self.selected_entities:
                            rels_with_both[key] = value
                        else:
                            rels_with_either[key] = value
                    elif pair[1] in self.selected_entities:
                        rels_with_either[key] = value

            if rels_with_both:
                relations_dict = rels_with_both
            else:
                relations_dict = rels_with_either

            selected_rels = []
            for key, value in relations_dict.items():
                if not value:
                    continue

                for pair in value:
                    if (
                        pair[0] in self.selected_entities
                        or pair[1] in self.selected_entities
                    ):
                        selected_rels.append((key, pair))

            relations_dict = json.dumps(selected_rels)
        else:
            relations_dict = json.dumps(self.relationships)

        msg = (
            "You have access to a knowledge graph that contains "
            f"these entities: {', '.join(self.selected_entities)}. "
            "Your task is to select the relationships that are relevant to the "
            "entities selected for your query. Only return the relationships, "
            "comma-separated, without any additional text. Do not return "
            "entity names, relationships, or properties."
        )

        msg, token_usage, correction = conversation.query(self.question)

        result = msg.split(",") if msg else []

        if result:
            for entity in result:
                entity = entity.strip()
                if entity in self.entities:
                    self.selected_relationships.append(entity)

        return bool(result)

    def _generate_query(
        self,
        question: str,
        entities: list,
        relationships: dict,
        properties: list,
        query_language: Optional[str] = "Cypher",
        conversation: "Conversation",
    ) -> str:
        """
        Generates a database query based on selected entities, relationships, and properties.

        Args:
            question: User's question.

            entities: Selected entities.

            relationships: Selected relationships.

            properties: Selected properties.

            query_language: Query language (default is Cypher).

            conversation: Conversation object.

        Returns:
            Generated database query.
        """
        return f"Generated query based on {', '.join(entities)}, {', '.join(relationships)}, {', '.join(properties)}"


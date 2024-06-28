from abc import ABC, abstractmethod
import json
import logging
import nltk  # Make sure nltk is properly installed and imported
from transformers import pipeline, BigScienceModule, BloomModule, GPT2Tokenizer, GPT2Model

class Conversation(ABC):
    def __init__(
        self,
        model_name_or_path: str,
        prompts: dict,
        correct: bool = True,
        split_correction: bool = False,
    ):
        super().__init__()
        self.model_name_or_path = model_name_or_path
        self.prompts = prompts
        self.correct = correct
        self.split_correction = split_correction
        self.history = []
        self.messages = []
        self.ca_messages = []
        self.current_statements = []
        self.pipeline = pipeline("conversational", model=self.model_name_or_path)
        self.bigscience_module = BigScienceModule()
        self.bloom_module = BloomModule()
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_name_or_path)
        self.model = GPT2Model.from_pretrained(model_name_or_path)

    def setup(self, context: str):
        self.append_system_message(f"The topic of the research is {context}.")
        self.setup_prompts()

    def setup_prompts(self):
        for msg in self.prompts.get("primary_model_prompts", []):
            if msg:
                self.append_system_message(msg)
        for msg in self.prompts.get("correcting_agent_prompts", []):
            if msg:
                self.append_ca_message(msg)

    def query(self, text: str) -> tuple[str, dict, str]:
        self.append_user_message(text)
        self.inject_context(text)
        msg = self.primary_query()

        if self.correct:
            correction = self.correct_query(text)
            return msg, None, correction
        else:
            return msg, None, None

    @abstractmethod
    def set_api_key(self, api_key: str, user: Optional[str] = None):
        pass

    @abstractmethod
    def primary_query(self) -> str:
        pass

    @abstractmethod
    def correct_query(self, msg: str) -> str:
        pass

    @abstractmethod
    def inject_context(self, text: str):
        pass

    def append_system_message(self, message: str) -> None:
        self.messages.append({"role": "system", "content": message})

    def append_ca_message(self, message: str) -> None:
        self.ca_messages.append({"role": "ca", "content": message})

    def append_user_message(self, message: str) -> None:
        self.messages.append({"role": "user", "content": message})

    def reset(self):
        self.history.clear()
        self.messages.clear()
        self.ca_messages.clear()
        self.current_statements.clear()

    def get_msg_json(self) -> str:
        return json.dumps(self.messages + self.ca_messages + self.history)

    def get_token_size(self, text: str) -> int:
        tokens = self.tokenizer.encode(text, add_special_tokens=False)
        return len(tokens)

# Example usage:
conversation = Conversation(model_name_or_path="gpt-4", prompts={})
context = "AI-driven drug discovery"
conversation.setup(context)
user_input = "What are the latest advancements in AI for drug discovery?"
response, _, _ = conversation.query(user_input)
token_size = conversation.get_token_size(user_input)
print(f"Response: {response}")
print(f"Token size: {token_size}")


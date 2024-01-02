
from typing import Any
# from promptengineers.core.validations import Validator
from promptengineers.core.config.llm import ACCEPTED_OLLAMA_MODELS, ACCEPTED_OPENAI_MODELS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.embeddings import OllamaEmbeddings

# validator = Validator()

class EmbeddingFactory:
	def __init__(self, llm: str, token: str = None, base_url: str = None):
		self.llm = llm
		self.token = token
		self.base_url = base_url

	def __call__(self) -> Any:
		if self.llm in ACCEPTED_OPENAI_MODELS:
			return OpenAIEmbeddings(openai_api_key=self.token)
		elif self.llm in ACCEPTED_OLLAMA_MODELS:
			return OllamaEmbeddings(base_url=self.base_url or 'http://127.0.0.1:11434')
		else:
			raise ValueError(f"Invalid embedding model {self.llm}")
					 
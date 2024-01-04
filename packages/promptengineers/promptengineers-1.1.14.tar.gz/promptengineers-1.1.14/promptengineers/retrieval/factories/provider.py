
from promptengineers.core.interfaces.repos import IUserRepo
from promptengineers.core.validations import Validator
from promptengineers.repos.user import UserRepo
from promptengineers.retrieval.strategies import PineconeStrategy, RedisStrategy

class RetreivalFactory:
	def __init__(
			self,
			provider: ('redis', 'pinecone'), 
			index_name: str,
			embeddings,
			user_id: str,
			user_repo: IUserRepo = UserRepo()
	):
		self.provider = provider
		self.index_name = index_name
		self.embeddings = embeddings
		self.user_id = user_id
		self.user_repo = user_repo
		self.validator = Validator()

	def __call__(self) -> PineconeStrategy | RedisStrategy:
		if self.provider in 'pinecone':
			required_keys = ['PINECONE_API_KEY', 'PINECONE_ENV', 'PINECONE_INDEX']
			tokens = self.user_repo.find_token(self.user_id, required_keys)
			self.validator.validate_api_keys(tokens, required_keys)
			vectorstore_strategy = PineconeStrategy(
				embeddings=self.embeddings,
				api_key=tokens.get(required_keys[0]),
				env=tokens.get(required_keys[1]),
				index_name=tokens.get(required_keys[2]),
				namespace=self.index_name,
			)
		elif self.provider in 'redis':
			required_keys = ['REDIS_URL']
			tokens = self.user_repo.find_token(self.user_id, required_keys)
			self.validator.validate_api_keys(tokens, required_keys)
			vectorstore_strategy = RedisStrategy(
				redis_url=tokens.get(required_keys[0]),
				index_name=self.index_name,
				embeddings=self.embeddings,
			)
		else:
			raise ValueError(f"Invalid index provider {self.provider}")
		return vectorstore_strategy
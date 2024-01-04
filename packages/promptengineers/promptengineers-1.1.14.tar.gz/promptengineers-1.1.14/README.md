# Prompt Engineers AI Open Source Package

### Build and Publish

```bash
## Build Package
bash scripts/build.sh

## Publish Package to PyPi
bash scripts/publish.sh
```


### Development

```bash
## In the application directory start your virtual env (this would be the workspace
## where your API server that you would like to install the model)
source .venv/bin/activate

## Then change directory to where your package is, make changes and run the following.
pip install .

## Switch back to the directory of your where your workspace is for you app server.
cd <path>/<app>/<server>
pip install -r requirements.txt

## Make sure your app server has the packages shown in setup.py and run your server...
```

## How to use...

### User Respository
A [User Repository](https://github.com/promptengineers-ai/llm-server/blob/master/server/repos/user.py) can be added to any application and then extended and then passed to llm-server to fetch user default project configurables via the 
environment variables or for multi-tenanted user application. This is allows for new variables when adding additional tools.

### Retrieval Augemented Generation (RAG) - HTTP Chat
```py
# Import necessary modules and classes
from promptengineers.core.config.test import TEST_USER_ID
from promptengineers.core.valdations import Validator
from promptengineers.retrieval.factories.provider VectorSearchProviderFactory
from promptengineers.retrieval.strategies import VectorstoreContext

from server.repos.user import UserRepo

INDEX_PROVIDER = 'pinecone'
INDEX_NAME = 'MyRetrievalIndex'
MODEL = 'gpt-4-turbo'
TEMPERATURE = 0.9,
MESSAGES = [
    {
        'role': 'system', 
        'content': 'You are a helpful document retrieval AI, use the context to answer the user queries.'
    },
    {
        'role': 'user', 
        'content': 'Can you summarize the context?'
    }
]

user_repo = UserRepo()

# Define a list of required API keys
required_keys = ['OPENAI_API_KEY', 'PINECONE_API_KEY', 'PINECONE_ENV', 'PINECONE_INDEX']

# Retrieve API tokens using the UserRepo class
tokens = user_repo.find_token(TEST_USER_ID, required_keys)

# Validate the retrieved API tokens against the required keys
Validator().validate_api_keys(tokens, required_keys)

# Choose the appropriate vector search provider strategy for Pinecone
vectorstore_strategy = VectorSearchProviderFactory.choose(
    provider=INDEX_PROVIDER,   # Specify the provider as 'pinecone'
    user_id=TEST_USER_ID,       # The user ID
    index_name=INDEX_NAME,  # The name of the index in Pinecone
    user_repo=user_repo   # An instance of UserRepo
)

# Create a vector store service context
vectostore_service = VectorstoreContext(vectorstore_strategy)

# Load the vectorstore using the service context
vectorstore = vectostore_service.load()

# Initialize a chat controller with a specific test user ID and user repository
chat_controller = ChatController(user_id=TEST_USER_ID, user_repo=user_repo)

# Conduct a chat using the langchain_http_vectorstore_chat method with specific parameters
result, cb = chat_controller.langchain_http_vectorstore_chat(
    messages=MESSAGES,
    model=MODEL,  # Specify the model to use (GPT-4 Turbo)
    temperature=TEMPERATURE,      # Set the temperature for response variability
    vectorstore=vectorstore,  # Use the previously loaded vectorstore
)
```
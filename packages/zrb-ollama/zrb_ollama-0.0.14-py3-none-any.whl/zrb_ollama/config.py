import os

DEFAULT_OLLAMA_BASE_URL = os.getenv(
    'ZRB_OLLAMA_BASE_URL', 'http://localhost:11434'
)
DEFAULT_MODEL = os.getenv('ZRB_OLLAMA_DEFAULT_MODEL', 'orca-mini')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')

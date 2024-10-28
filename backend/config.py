# backend/config.py

import os
from dotenv import load_dotenv
from key import api_key

# Flask Configuration
DEBUG = True
PORT = 5000

# Model Configuration
ANTHROPIC_API_KEY = api_key
MODEL_NAME = 'llama3.2:latest'

# Available Models
AVAILABLE_MODELS = {
    'llama': {
        'name': 'Llama 3.2',
        'handler': 'LlamaHandler'
    },
    'claude': {
        'name': 'Claude 3 Sonnet',
        'handler': 'ClaudeHandler'
    }
}

DEFAULT_MODEL = 'llama'

# Chat Configuration
MAX_RECENT_MESSAGES = 5
MAX_TOKENS = 10000
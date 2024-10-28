# backend/model_handlers.py

from anthropic import Anthropic
import ollama
from abc import ABC, abstractmethod
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ModelHandler(ABC):
    @abstractmethod
    def generate_response(self, messages, stream=True):
        pass

class LlamaHandler(ModelHandler):
    def generate_response(self, messages, stream=True):
        try:
            for chunk in ollama.chat(
                model='llama3.2:latest',
                messages=messages,
                stream=stream
            ):
                yield {'content': chunk['message']['content']}
        except Exception as e:
            logger.error(f"Error in LlamaHandler: {str(e)}")
            yield {'error': str(e)}

class ClaudeHandler(ModelHandler):
    def __init__(self, api_key):
        try:
            self.client = Anthropic(api_key=api_key)
            logger.debug("Claude client initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing Claude client: {str(e)}")
            raise
        
    def generate_response(self, messages, stream=True):
        try:
            # Convert messages to the format expected by Anthropic
            formatted_messages = []
            for msg in messages:
                if msg['role'] == 'system':
                    # Handle system messages by prepending to the first user message
                    continue
                formatted_messages.append({
                    'role': msg['role'],
                    'content': msg['content']
                })
            
            # If there was a system message, prepend it to the first user message
            system_message = next((msg['content'] for msg in messages if msg['role'] == 'system'), None)
            if system_message and formatted_messages:
                for msg in formatted_messages:
                    if msg['role'] == 'user':
                        msg['content'] = f"{system_message}\n\n{msg['content']}"
                        break
            
            logger.debug(f"Sending request to Claude with {len(formatted_messages)} messages")
            
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1024,
                temperature=0.7,
                messages=formatted_messages,
                stream=stream
            )
            
            if stream:
                for chunk in response:
                    if chunk.type == 'content_block_delta':
                        yield {'content': chunk.delta.text}
            else:
                yield {'content': response.content[0].text}
                
        except Exception as e:
            logger.error(f"Error in ClaudeHandler: {str(e)}")
            yield {'error': str(e)}
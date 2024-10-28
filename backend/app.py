from flask import Flask, request, jsonify, render_template, Response
from flask_cors import CORS
import ollama
import time
import sys
from chat_manager import get_optimized_context, summarize_conversation
from prompt_manager import PromptManager
import config
import json
from model_handlers import LlamaHandler, ClaudeHandler
import json

app = Flask(__name__,
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
CORS(app)

# Store conversations in memory (replace with database for production)
conversations = {}

@app.route('/api/models', methods=['GET'])
def get_models():
    return jsonify({
        'models': config.AVAILABLE_MODELS,
        'default': config.DEFAULT_MODEL
    })

def print_streaming(text):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(0.01)

def detect_prompt_type(message):
    """Detect the type of prompt based on the message content"""
    message_lower = message.lower()
    
    # Check for project development request
    if any(keyword in message_lower for keyword in ['create project', 'develop', 'build application', 'make app']):
        return 'project'
    # Check for code request
    elif any(keyword in message_lower for keyword in ['code', 'function', 'class', 'program']):
        return 'code'
    else:
        return 'default'

def get_system_prompt(message):
    """Get appropriate system prompt based on message content"""
    prompt_type = detect_prompt_type(message)
    
    if prompt_type == 'project':
        # Example tech stack - you can modify this based on the project needs
        tech_stack = """
        - Flask
        - SQLite
        - Flask-SQLAlchemy
        - Basic HTML/CSS
        - JWT for authentication
        - Logging
        """
        return PromptManager.get_project_prompt(
            project_name=message,
            tech_stack=tech_stack
        )
    elif prompt_type == 'code':
        return PromptManager.get_code_prompt()
    else:
        return PromptManager.get_default_prompt()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message')
        session_id = data.get('session_id', 'default')
        model_id = data.get('model', config.DEFAULT_MODEL)
        
        if session_id not in conversations:
            conversations[session_id] = []
        
        # Get appropriate system prompt
        system_prompt = get_system_prompt(user_message)
        
        # Add or update system prompt
        if not conversations[session_id]:
            conversations[session_id].append({
                'role': 'system',
                'content': system_prompt
            })
        else:
            conversations[session_id][0] = {
                'role': 'system',
                'content': system_prompt
            }
        
        # Add user message
        conversations[session_id].append({
            'role': 'user',
            'content': user_message
        })
        
        # Get optimized context
        optimized_context = get_optimized_context(conversations[session_id])
        
        # Get appropriate model handler
        model_config = config.AVAILABLE_MODELS.get(model_id)
        if not model_config:
            return jsonify({'error': 'Invalid model selection'}), 400
        
        try:
            handler_class = globals()[model_config['handler']]
            handler = handler_class(config.ANTHROPIC_API_KEY) if model_id == 'claude' else handler_class()
            
            def generate():
                full_response = ""
                try:
                    for chunk in handler.generate_response(optimized_context):
                        if 'error' in chunk:
                            error_msg = f"Model error: {chunk['error']}"
                            app.logger.error(error_msg)
                            yield f"data: {json.dumps({'error': error_msg})}\n\n"
                            return
                        
                        chunk_content = chunk['content']
                        full_response += chunk_content
                        yield f"data: {json.dumps({'content': chunk_content})}\n\n"
                    
                    # Add assistant response to conversation
                    conversations[session_id].append({
                        'role': 'assistant',
                        'content': full_response
                    })
                    
                except Exception as e:
                    error_msg = f"Streaming error: {str(e)}"
                    app.logger.error(error_msg)
                    yield f"data: {json.dumps({'error': error_msg})}\n\n"
            
            return Response(generate(), mimetype='text/event-stream')
            
        except Exception as e:
            error_msg = f"Handler initialization error: {str(e)}"
            app.logger.error(error_msg)
            return jsonify({'error': error_msg}), 500
            
    except Exception as e:
        error_msg = f"General error: {str(e)}"
        app.logger.error(error_msg)
        return jsonify({'error': error_msg}), 500

@app.route('/api/clear', methods=['POST'])
def clear_conversation():
    try:
        data = request.json
        session_id = data.get('session_id', 'default')
        conversations[session_id] = []
        return jsonify({'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=config.DEBUG, port=config.PORT)
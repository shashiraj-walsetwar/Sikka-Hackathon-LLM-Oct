import ollama
import time
import sys
import ast
import os
import re
import json

def get_llm_response(prompt):
   try:
       print("\nThinking and generating code for your application...")
       response = ollama.chat(
           model='llama3.2:latest',
           messages=[{'role': 'user', 'content': prompt}],
           stream=False
       )
       print("Code generation completed!")
       
       # Write raw response to file
       print("\nWriting response to 'raw_response.txt'...")
       with open('raw_response.txt', 'w', encoding='utf-8') as f:
           f.write(response['message']['content'])
       print("Response saved to 'raw_response.txt'")
       
       return response['message']['content']
   except Exception as e:
       print(f"An error occurred: {e}")
       return None

def clean_response(text):
    """Clean the response text of common formatting issues."""
    # Remove markdown code blocks
    text = re.sub(r'```.*?\n', '', text)
    text = re.sub(r'```', '', text)
    
    # Remove YAML-style formatting
    text = re.sub(r'\s*\|\s*', '', text)
    
    # Find the dictionary content
    dict_match = re.search(r'\{.*\}', text, re.DOTALL)
    if not dict_match:
        raise ValueError("No dictionary found in response")
    
    dict_text = dict_match.group(0)
    
    try:
        # Parse as JSON first to handle escaping properly
        dict_data = json.loads(dict_text)
        # Convert back to a properly formatted Python dictionary string
        return repr(dict_data)
    except json.JSONDecodeError:
        # If JSON parsing fails, try cleaning the string manually
        dict_text = re.sub(r'\\(?![nrt"])', r'\\\\', dict_text)
        dict_text = dict_text.replace('\\"', '"')
        dict_text = dict_text.replace('"', '\\"')
        dict_text = re.sub(r',(\s*})', r'\1', dict_text)
        return dict_text

def string_to_dict(response_string):
   try:
       print("\nProcessing the generated code...")
       # Clean and process the response
       cleaned_response = clean_response(response_string)
           
       # Write cleaned response to file
       print("\nWriting cleaned response to 'cleaned_response.txt'...")
       with open('cleaned_response.txt', 'w', encoding='utf-8') as f:
           f.write(cleaned_response)
       print("Cleaned response saved to 'cleaned_response.txt'")
           
       # Try to parse the dictionary
       try:
           result = ast.literal_eval(cleaned_response)
       except Exception as e:
           print(f"Parsing error: {e}")
           print("Raw dictionary string:")
           print(cleaned_response[:500])
           raise
           
       print("Processing completed!")
       return result
   except Exception as e:
       print(f"Error converting string to dict: {e}")
       print("\nError details:")
       print(f"Response type: {type(response_string)}")
       print(f"Response preview: {response_string[:500]}...")
       print("\nPlease try running the program again.")
       return None

def create_files(file_dict, project_name):
   print(f"\nCreating project directory: {project_name}")
   try:
       # Create main project directory
       os.makedirs(project_name, exist_ok=True)
   except Exception as e:
       print(f"Error creating project directory: {e}")
       return

   print("\nStarting to create files...")
   for filepath, content in file_dict.items():
       try:
           # Combine project directory with file path
           full_path = os.path.join(project_name, filepath)
           # Create all necessary subdirectories
           directory = os.path.dirname(full_path)
           if directory:
               os.makedirs(directory, exist_ok=True)
               print(f"Created directory: {directory}")
           
           with open(full_path, 'w', encoding='utf-8') as f:
               f.write(content)
           print(f"Created file: {full_path}")
       except Exception as e:
           print(f"Error creating file {full_path}: {e}")
   print("\nAll files have been created successfully!")

# Updated prompt to ensure proper JSON formatting
base_prompt = """You are an expert Python developer. Create a complete {application_type} that can be used by any practice. Return ONLY a JSON-formatted dictionary containing the files and their contents.

The dictionary format MUST be exactly like this:
{{{{
    "app/main.py": "from flask import Flask\\nimport os\\n\\napp = Flask(__name__)\\n",
    "app/models.py": "from flask_sqlalchemy import SQLAlchemy\\n\\ndb = SQLAlchemy()\\n",
    "requirements.txt": "Flask==2.0.1\\nSQLAlchemy==1.4.23"
}}}}

The system must be built using:
- Flask 
- SQLite
- Flask-SQLAlchemy
- Basic HTML/CSS

Required functionality:
- User authentication
- Patient/client management
- Appointment scheduling
- Medical records
- Basic frontend templates

Create ALL necessary files including:
- Python files (.py)
- HTML templates (.html)
- CSS stylesheets (.css) 
- Database models
- Configuration files
- Requirements.txt

CRITICAL FORMATTING RULES:
1. Return ONLY the dictionary/JSON object
2. NO explanation text or markdown
3. Use double quotes for all strings
4. Escape newlines as \\n
5. Escape quotes properly
6. No trailing commas
7. Format must be valid JSON"""

# Get user input
print("Welcome to Application Generator!")
print("What kind of application would you like to create?")
app_type = input("Application type (e.g., reputation management system): ")
project_name = input("Project name (this will be your directory name): ")

# Format the prompt with user input
final_prompt = base_prompt.format(application_type=app_type)

# Get response from LLM
response = get_llm_response(final_prompt)

# Convert string to dict
if response:
   file_dict = string_to_dict(response)
   
   # Create files in the project directory
   if file_dict:
       create_files(file_dict, project_name)

print("\nProcess completed!" if not response else "")
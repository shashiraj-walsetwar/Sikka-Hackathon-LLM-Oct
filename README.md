# Healthcare Practice Management API Integration Platform

A Flask-based web application that provides a chat interface for integrating with Sikka Healthcare APIs and various AI models (Llama and Claude). The platform facilitates seamless integration with healthcare practice management systems through a comprehensive API suite.

## 🚀 Features

Interactive chat interface for API interactions
Support for multiple AI models (Llama 3.2 and Claude 3 Sonnet)
Real-time streaming responses
Comprehensive Sikka API integration
Code syntax highlighting
Conversation management
Context-aware responses

## 📋 Prerequisites

Python 3.8 or higher
Ollama (for Llama model)
Anthropic API key (for Claude model)

## 🛠️ Installation

Clone the repository

```
git clone https://github.com/shashiraj-walsetwar/Sikka-Hackathon-LLM-Oct.git
git checkout Integration-with-Sikka-API-documentation
cd Sikka-Hackathon-LLM-Oct
```

Create and activate a virtual environment

```python -m venv venv
.\venv\Scripts\activate
```

Install Python dependencies

```
pip install -r requirements.txt
```


## 📁 Project Structure

.
├── backend/
│   ├── __init__.py
│   ├── app.py                 # Main Flask application
│   ├── api_documentation.py   # Sikka API documentation
│   ├── chat_manager.py       # Chat context management
│   ├── config.py             # Configuration settings
│   ├── model_handlers.py     # AI model handlers
│   └── prompt_manager.py     # Prompt templates
├── frontend/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css    # Main stylesheet
│   │   └── js/
│   │       └── main.js      # Frontend JavaScript
│   └── templates/
│       └── index.html       # Main HTML template
└── README.md

## 🔌 Available APIs

The platform integrates all the essential Sikka Healthcare APIs for software development and data extraction.

## 🚦 Running the Application

Start the Flask backend

```
python backend/app.py
```

Access the application

Open your browser and navigate to: http://localhost:5000

## 🤖 Supported AI Models

### Llama 3.2

- Default model
- Runs locally using Ollama
- No API key required


### Claude 3 Sonnet

- Advanced language model by Anthropic
- Requires API key
- Better at complex reasoning tasks

## Developed By- Manali Naik(manali.naik@sikka.ai) & Shashiraj Walsetwar(shashiraj.walsetwar@sikka.ai)
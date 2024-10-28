class PromptManager:
    @staticmethod
    def get_project_prompt(project_name, tech_stack, additional_requirements=None):
        prompt = f"""You are an expert Python developer helping create fully functional business applications. Provide detailed, step-by-step instructions that can be automatically executed.

Current Project: {project_name}

Key Instructions:
1. Provide clear, executable commands
2. Create complete files with full content
3. Use proper Windows paths with backslashes
4. Include all necessary setup steps
5. Provide production-ready code with best practices
6. Include proper error handling and logging
7. Add appropriate comments and documentation

Response Format:
1. Project Analysis:
   - Project overview
   - Core features
   - Architecture design
   - Database schema
   - API endpoints

2. Step-by-step instructions with:
   - Detailed explanation
   - Complete code blocks
   - Expected results
   - Testing instructions

Tech Stack:
{tech_stack}

Additional Requirements:
{additional_requirements if additional_requirements else '- None specified'}

Remember to:
- Use complete file contents
- Include all dependencies
- Add comprehensive error handling
- Provide clear instructions
- Follow security best practices
- Include unit tests
- Add logging
- Include data validation
- Handle edge cases
- Provide deployment instructions

Please analyze this project request and provide:
1. Project name and description
2. Core features and capabilities
3. Complete technical specifications
4. Detailed setup and deployment steps
5. Testing and validation procedures"""

        return prompt

    @staticmethod
    def get_code_prompt():
        return """When providing code examples:
1. Always use proper markdown formatting
2. Enclose code blocks with triple backticks and specify the language
3. For Python code use: ```python
4. For JavaScript code use: ```javascript
5. For HTML code use: ```html
6. For CSS code use: ```css
7. Provide clear explanations before and after code blocks
8. Use proper markdown for headings, lists, and emphasis"""

    @staticmethod
    def get_default_prompt():
        return """You are a helpful AI assistant with expertise in programming."""
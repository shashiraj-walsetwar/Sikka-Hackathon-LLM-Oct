import ollama
from config import MAX_RECENT_MESSAGES, MAX_TOKENS, MODEL_NAME

def summarize_conversation(conversation):
    conversation_text = ""
    for msg in conversation:
        role = msg['role'].capitalize()
        content = msg['content']
        conversation_text += f"{role}: {content}\n"
    
    summarization_prompt = [
        {
            'role': 'system',
            'content': 'Create a brief summary (2-3 sentences) of the key points from the following conversation.'
        },
        {
            'role': 'user',
            'content': f"Please summarize this conversation:\n\n{conversation_text}"
        }
    ]
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=summarization_prompt,
            stream=False
        )
        return response['message']['content'].strip()
    except Exception as e:
        return f"Conversation with {len(conversation)} messages about various topics."

def get_optimized_context(conversation, max_recent_messages=MAX_RECENT_MESSAGES, max_tokens=MAX_TOKENS):
    if len(conversation) <= max_recent_messages:
        return conversation

    context = []
    
    if len(conversation) > max_recent_messages:
        earlier_conversation = conversation[:-max_recent_messages]
        summary = summarize_conversation(earlier_conversation)
        context.append({'role': 'system', 'content': f"Earlier conversation summary: {summary}"})
    
    context.extend(conversation[-max_recent_messages:])
    
    total_tokens = sum(len(message['content'].split()) for message in context)
    
    while total_tokens > max_tokens and len(context) > 1:
        removed_message = context.pop(1)
        total_tokens -= len(removed_message['content'].split())
    
    return context
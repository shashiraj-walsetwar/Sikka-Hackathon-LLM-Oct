// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const clearButton = document.getElementById('clear-chat');



// Generate a random session ID
const sessionId = Math.random().toString(36).substring(7);

let currentModel = null;

// Add function to load available models
async function loadAvailableModels() {
    try {
        const response = await fetch('/api/models');
        const data = await response.json();
        
        const modelSelector = document.getElementById('model-selector');
        modelSelector.innerHTML = '';
        
        Object.entries(data.models).forEach(([id, model]) => {
            const option = document.createElement('option');
            option.value = id;
            option.textContent = model.name;
            modelSelector.appendChild(option);
        });
        
        // Set default model
        currentModel = data.default;
        modelSelector.value = currentModel;
    } catch (error) {
        console.error('Error loading models:', error);
    }
}

// Function to check if chat is scrolled to bottom
function isAtBottom() {
    const threshold = 100; // pixels from bottom to consider "at bottom"
    return (chatMessages.scrollHeight - chatMessages.scrollTop - chatMessages.clientHeight) < threshold;
}

// Smart scroll function
function smartScroll() {
    if (isAtBottom()) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
}

// Add message to chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(isUser ? 'user-message' : 'assistant-message');
    
    if (isUser) {
        messageDiv.textContent = content;
    } else {
        // For code blocks and markdown
        let formattedContent = content.replace(/```(\w+)?\n([\s\S]*?)```/g, function(match, language, code) {
            language = language || '';
            return `<pre><code class="language-${language}">${code}</code></pre>`;
        });
        messageDiv.innerHTML = formattedContent;
    }
    
    chatMessages.appendChild(messageDiv);
    smartScroll();
    return messageDiv;
}

// Show typing indicator
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.classList.add('typing-indicator', 'message', 'assistant-message');
    indicator.textContent = 'AI is typing...';
    indicator.id = 'typing-indicator';
    chatMessages.appendChild(indicator);
    smartScroll();
}

// Hide typing indicator
function hideTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Send message to backend
async function sendMessage(message) {
    try {
        showTypingIndicator();
        const responseDiv = addMessage('', false);
        hideTypingIndicator();

        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                model: currentModel
            })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let fullResponse = '';
        let wasAtBottom = isAtBottom(); // Store initial scroll position

        while (true) {
            const { value, done } = await reader.read();
            if (done) break;
            
            const text = decoder.decode(value);
            const lines = text.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        if (data.content) {
                            fullResponse += data.content;
                            // Format the content with code highlighting
                            let formattedContent = fullResponse.replace(/```(\w+)?\n([\s\S]*?)```/g, function(match, language, code) {
                                language = language || '';
                                return `<pre><code class="language-${language}">${code}</code></pre>`;
                            });
                            responseDiv.innerHTML = formattedContent;
                            
                            // Apply Prism highlighting
                            responseDiv.querySelectorAll('pre code').forEach((block) => {
                                Prism.highlightElement(block);
                            });
                            
                            // Only scroll if we were at the bottom initially
                            if (wasAtBottom) {
                                smartScroll();
                            }
                        } else if (data.error) {
                            responseDiv.textContent = `Error: ${data.error}`;
                        }
                    } catch (e) {
                        console.error('Error parsing SSE data:', e);
                    }
                }
            }
        }

    } catch (error) {
        hideTypingIndicator();
        addMessage('Sorry, there was an error processing your message. Please try again.');
        console.error('Error:', error);
    }
}
// Add model selector event listener
document.getElementById('model-selector').addEventListener('change', (e) => {
    currentModel = e.target.value;
});

// Load models when page loads
document.addEventListener('DOMContentLoaded', loadAvailableModels);

// Clear chat
async function clearChat() {
    try {
        const response = await fetch('/api/clear', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                session_id: sessionId
            })
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        chatMessages.innerHTML = '';
    } catch (error) {
        console.error('Error clearing chat:', error);
    }
}

// Event Listeners
sendButton.addEventListener('click', () => {
    const message = userInput.value.trim();
    if (message) {
        addMessage(message, true);
        sendMessage(message);
        userInput.value = '';
    }
});

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendButton.click();
    }
});

clearButton.addEventListener('click', clearChat);

// Add scroll listener to update wasAtBottom state
chatMessages.addEventListener('scroll', () => {
    wasAtBottom = isAtBottom();
});

// Initialize Prism.js
Prism.highlightAll();
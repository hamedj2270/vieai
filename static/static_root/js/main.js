// Chat functionality
let currentMessageId = null;
let responseCheckInterval = null;

function toggleChat() {
    document.getElementById('chatWindow').classList.toggle('active');
}

function sendMessage(event) {
    event.preventDefault();
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    
    if (message) {
        // Add user message
        addMessage(message, 'user');
        input.value = '';
        
        // Send message to server
        fetch('/livechat/send_message/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({
                message: message
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                currentMessageId = data.message_id;
                addMessage(data.response, 'bot');
                // شروع بررسی پاسخ تلگرام
                startCheckingResponse();
            } else {
                addMessage('متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.', 'bot');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            addMessage('متأسفانه خطایی رخ داد. لطفاً دوباره تلاش کنید.', 'bot');
        });
    }
}

function startCheckingResponse() {
    if (responseCheckInterval) {
        clearInterval(responseCheckInterval);
    }
    
    responseCheckInterval = setInterval(() => {
        if (currentMessageId) {
            fetch(`/livechat/get_response/${currentMessageId}/`)
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        addMessage(data.response, 'bot');
                        clearInterval(responseCheckInterval);
                        currentMessageId = null;
                    }
                })
                .catch(error => {
                    console.error('Error checking response:', error);
                    clearInterval(responseCheckInterval);
                    currentMessageId = null;
                });
        }
    }, 3000); // بررسی هر 3 ثانیه
}

function addMessage(text, type) {
    const messagesDiv = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    messagesDiv.appendChild(messageDiv);
    messagesDiv.scrollTop = messagesDiv.scrollHeight;
}

// Get CSRF token from cookie
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Product description toggle
function toggleDescription(productId) {
    const description = document.getElementById(`description-${productId}`);
    const button = description.nextElementSibling;
    
    if (description.classList.contains('truncated')) {
        description.classList.remove('truncated');
        button.textContent = 'کمتر';
    } else {
        description.classList.add('truncated');
        button.textContent = 'بیشتر';
    }
} 
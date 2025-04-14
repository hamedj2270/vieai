// Chat functionality
let currentMessageId = null;
let responseCheckInterval = null;

function toggleChat() {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.classList.toggle('active');
}

function sendMessage(event) {
    event.preventDefault();
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, 'user');
    messageInput.value = '';
    
    // Send message to server
    fetch('/livechat/send_message/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            currentMessageId = data.message_id;
            startCheckingResponse();
        } else {
            addMessage('متأسفانه در ارسال پیام مشکلی پیش آمده. لطفاً دوباره تلاش کنید.', 'bot');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('متأسفانه در ارسال پیام مشکلی پیش آمده. لطفاً دوباره تلاش کنید.', 'bot');
    });
}

function startCheckingResponse() {
    if (responseCheckInterval) {
        clearInterval(responseCheckInterval);
    }
    
    responseCheckInterval = setInterval(() => {
        if (!currentMessageId) return;
        
        fetch(`/livechat/get_response/${currentMessageId}/`)
            .then(response => response.json())
            .then(data => {
                if (data.success && data.response) {
                    addMessage(data.response, 'bot');
                    clearInterval(responseCheckInterval);
                    currentMessageId = null;
                }
            })
            .catch(error => {
                console.error('Error:', error);
                clearInterval(responseCheckInterval);
                currentMessageId = null;
            });
    }, 3000);
}

function addMessage(text, type) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = text;
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

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
    if (description.classList.contains('truncated')) {
        description.classList.remove('truncated');
    } else {
        description.classList.add('truncated');
    }
} 
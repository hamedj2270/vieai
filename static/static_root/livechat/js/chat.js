document.addEventListener('DOMContentLoaded', function() {
    const chatButton = document.querySelector('.chat-button');
    const chatWindow = document.querySelector('.chat-window');
    const closeButton = document.querySelector('.chat-close');
    const messageInput = document.querySelector('.chat-input input');
    const sendButton = document.querySelector('.chat-input button');
    const messagesContainer = document.querySelector('.chat-messages');
    const typingIndicator = document.querySelector('.typing-indicator');

    // Toggle chat window
    chatButton.addEventListener('click', () => {
        chatWindow.classList.toggle('active');
        if (chatWindow.classList.contains('active')) {
            messageInput.focus();
        }
    });

    closeButton.addEventListener('click', () => {
        chatWindow.classList.remove('active');
    });

    // Send message
    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        addMessage(message, 'user');
        messageInput.value = '';

        // Show typing indicator
        typingIndicator.classList.add('active');

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
            // Hide typing indicator
            typingIndicator.classList.remove('active');

            // Add bot response to chat
            if (data.success) {
                addMessage(data.response, 'bot');
            } else {
                addMessage('متأسفانه در ارسال پیام مشکلی پیش آمده. لطفاً دوباره تلاش کنید.', 'bot');
            }
        })
        .catch(error => {
            // Hide typing indicator
            typingIndicator.classList.remove('active');

            // Show error message
            addMessage('متأسفانه در ارسال پیام مشکلی پیش آمده. لطفاً دوباره تلاش کنید.', 'bot');
            console.error('Error:', error);
        });
    }

    // Send message on button click
    sendButton.addEventListener('click', sendMessage);

    // Send message on Enter key
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });

    // Add message to chat
    function addMessage(text, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.textContent = text;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
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
}); 
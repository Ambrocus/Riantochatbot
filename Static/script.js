document.getElementById('send-btn').addEventListener('click', function() {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value.trim();

    if (userMessage) {
        // Add user message to the chat
        const userMessageElement = document.createElement('div');
        userMessageElement.classList.add('message', 'sent');
        userMessageElement.innerHTML = `<p>${userMessage}</p>`;
        document.getElementById('chat-box').appendChild(userMessageElement);

        // Add bot response (simple example)
        const botMessageElement = document.createElement('div');
        botMessageElement.classList.add('message', 'received');
        botMessageElement.innerHTML = `<p>Received: ${userMessage}</p>`; // You can replace this with real logic or API calls
        document.getElementById('chat-box').appendChild(botMessageElement);

        // Scroll to bottom
        document.getElementById('chat-box').scrollTop = document.getElementById('chat-box').scrollHeight;

        // Clear input field
        inputField.value = '';
    }
});

// Optional: Allow pressing "Enter" to send the message
document.getElementById('user-input').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
        document.getElementById('send-btn').click();
    }
});

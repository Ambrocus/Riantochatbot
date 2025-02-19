document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('user-input').addEventListener('keydown', function (e) {
    if (e.key === 'Enter') sendMessage();
});

function sendMessage() {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value.trim();

    if (userMessage) {
        appendMessage(userMessage, 'sent');

        // Simulated bot response (Replace this with actual API call or response logic)
        setTimeout(() => {
            appendMessage("I'm here to help!", 'received');
        }, 1000);

        inputField.value = '';
        scrollChatToBottom();
    }
}

function appendMessage(message, type) {
    const chatBox = document.getElementById('chat-box');
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', type);
    messageElement.innerHTML = `<p>${message}</p>`;
    chatBox.appendChild(messageElement);
}

function scrollChatToBottom() {
    const chatBox = document.getElementById('chat-box');
    chatBox.scrollTop = chatBox.scrollHeight;
}

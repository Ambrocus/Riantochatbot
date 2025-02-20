function sendMessage() {
    const inputField = document.getElementById('user-input');
    const userMessage = inputField.value.trim();

    if (!userMessage) return;  // If input is empty, do nothing

    // Append user message to chat
    appendMessage(userMessage, 'sent');

    // 🔥 This is the fetch() function that sends data to the backend
    fetch('https://lazychat.onrender.com/chat', {  
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),  // Send user input
    })
    .then(response => response.json())  // Convert response to JSON
    .then(data => {
        console.log('Bot response:', data);  // Debugging log
        appendMessage(data.response, 'received');  // Display bot response
    })
    .catch(error => {
        console.error('Error:', error);  // Debugging error log
        appendMessage("Sorry, I couldn't process that. Please try again.", 'received');
    });

    inputField.value = '';  // Clear input field after sending
}
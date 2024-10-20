const socket = io();
let username = '';

document.getElementById('join').onclick = () => {
    const usernameInput = document.getElementById('username');
    username = usernameInput.value.trim();
    if (username) {
        socket.emit('join', username);
        document.getElementById('username-modal').style.display = 'none'; // Hide modal
    }
};

// Handle message sending
document.getElementById('send').onclick = () => {
    const messageInput = document.getElementById('message');
    const message = messageInput.value.trim();
    if (message) {
        socket.emit('send_message', message);
        messageInput.value = ''; // Clear input after sending
    }
};

// Display incoming messages
socket.on('message', (msg) => {
    const messagesDiv = document.getElementById('messages');
    messagesDiv.innerHTML += `<div>${msg}</div>`;
});

// Show username modal on load
window.onload = () => {
    document.getElementById('username-modal').style.display = 'block';
};

from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO, emit, disconnect
import os
import time
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

socketio = SocketIO(app)

clients = {}
spam_tracker = {}

USERNAME_CAP = 15
SPAM_TIME_LIMIT = 2  # seconds
SPAM_LIMIT = 5  # messages within the time limit

# List of banned words (add more as needed)
banned_words = [
    "nigger", "nigga", "chink", "faggot", "dyke",
    "spic", "wetback", "gook", "kike", "bitch",
    "tranny", "whore", "slut", "cunt", "bastard",
    "paki", "raghead", "redskin", "slant", "beaner",
    "zipperhead", "honky", "cracker", "wop", "yid",
    "queer", "homo", "pansy", "sissy", "freak"
]

def log_alert(alert_message):
    """Log alerts to a file."""
    with open('alert_log.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {alert_message}\n")

def log_user_info(username, ip_address, device_info):
    """Log user info when they join."""
    with open('user_log.txt', 'a') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - User: {username}, IP: {ip_address}, Device: {device_info}\n")

def censor_text(text):
    """Censor banned words with hashtags."""
    for word in banned_words:
        text = re.sub(rf'\b{re.escape(word)}\b', '#' * len(word), text, flags=re.IGNORECASE)
    return text

def can_send_message(username):
    """Check if the user can send a message based on spam limit."""
    current_time = time.time()
    if username not in spam_tracker:
        spam_tracker[username] = []

    spam_tracker[username] = [t for t in spam_tracker[username] if current_time - t < SPAM_TIME_LIMIT]

    if len(spam_tracker[username]) >= SPAM_LIMIT:
        return False

    spam_tracker[username].append(current_time)
    return True

@app.route('/')
def index():
    return render_template('chat.html')

@socketio.on('join')
def handle_join(username):
    ip_address = request.remote_addr
    device_info = request.user_agent.string
    if ' ' in username or len(username) > USERNAME_CAP or any(word in username.lower() for word in banned_words):
        alert_message = f"Banned username attempt: {username}, IP: {ip_address}"
        log_alert(alert_message)
        emit('message', 'Invalid username. No spaces, max length is 15 characters, and no offensive words.', broadcast=False)
        return

    if username in clients.values():
        emit('message', f'Username "{username}" is already taken. Please re-enter.', broadcast=False)
        return

    clients[request.sid] = username
    log_user_info(username, ip_address, device_info)
    emit('message', f'{username} has joined the chat!', broadcast=True)

@socketio.on('send_message')
def handle_message(data):
    username = clients.get(request.sid)
    if username is None:
        emit('message', 'You need to join the chat first.', broadcast=False)
        return

    msg = data['message']
    ip_address = request.remote_addr

    if not can_send_message(username):
        emit('message', 'You are sending messages too quickly. Please wait.', broadcast=False)
        return

    if any(word in msg.lower() for word in banned_words):
        alert_message = f"Banned word used: '{msg}' by {username}, IP: {ip_address}"
        log_alert(alert_message)
        emit('message', 'Your message contains inappropriate content.', broadcast=False)
        return

    if msg.startswith('/'):
        handle_command(msg, username)
    else:
        censored_msg = censor_text(msg)
        emit('message', f'{username}: {censored_msg}', broadcast=True)

def handle_command(command, username):
    if command == '/help':
        emit('message', 'Available commands: /help, /list, /msg <user>, /leave, /roll, /joke', broadcast=True)
    elif command == '/list':
        emit('message', 'Active users: ' + ', '.join(clients.values()), broadcast=True)
    elif command.startswith('/msg '):
        parts = command.split(' ', 2)
        target_user = parts[1]
        private_message = parts[2] if len(parts) > 2 else ''
        target_sid = [sid for sid, name in clients.items() if name == target_user]
        if target_sid:
            emit('message', f'Private from {username}: {private_message}', room=target_sid[0])
        else:
            emit('message', f'User {target_user} not found.', broadcast=True)
    elif command == '/leave':
        disconnect()
        emit('message', f'{username} has left the chat.', broadcast=True)
    elif command == '/roll':
        import random
        roll = random.randint(1, 6)
        emit('message', f'{username} rolled a {roll}.', broadcast=True)
    elif command == '/joke':
        emit('message', 'Why did the scarecrow win an award? Because he was outstanding in his field!', broadcast=True)
    elif command == '/upload':
        emit('message', 'Uploads are broken right now, use Google Drive links', broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    username = clients.pop(request.sid, 'Unknown')
    emit('message', f'{username} has left the chat.', broadcast=True)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    socketio.run(app, port=6968, debug=True)

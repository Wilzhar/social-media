const chatID = JSON.parse(document.getElementById('chat-id').textContent);
const userID = JSON.parse(document.getElementById('user-id').textContent);

const chatSocket = new WebSocket(
    'ws://'
    + window.location.host
    + '/ws/conversation/chat/'
    + chatID
    + '/'
);

chatSocket.onmessage = function (e) {
    const data = JSON.parse(e.data);
    document.querySelector('#chat-log').value += (data.message + '\n');
};

chatSocket.onclose = function (e) {
    console.error('Chat socket closed unexpectedly');
};

document.querySelector('#chat-message-input').focus();
document.querySelector('#chat-message-input').onkeyup = function (e) {
    if (e.key === 'Enter') {  // enter, return
        e.preventDefault();
        document.querySelector('#chat-message-submit').click();
    }
};

document.querySelector('#chat-message-submit').onclick = function (e) {
    const messageInputDom = document.querySelector('#chat-message-input');
    const message = messageInputDom.value;
    chatSocket.send(JSON.stringify({
        'message': message,
        'user_id': userID,
        'chat_id': chatID
    }));
    messageInputDom.value = ''
};

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

    var ul = document.getElementById("chat-log");
    var li = document.createElement("li");
    li.appendChild(document.createTextNode(data.message));
    if (userID == data.user_id) {
        li.classList.add("bg-[#7743DB]", "text-white", "my-2", "p-2", "w-3/5", "ml-auto", "mr-0");
    } else {
        li.classList.add("bg-[#C3ACD0]", "text-white", "my-2", "p-2", "w-3/5", "ml-0", "mr-auto");
    }
    ul.appendChild(li);
    window.scrollBy(0, window.innerHeight);
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
    window.scrollBy(0, window.innerHeight);
};


function windowResized() {
    const parent = document.querySelector(".parent");
    document.querySelector(".child").style.width = `${parent.clientWidth - 16}px`;
}

window.addEventListener("resize", windowResized);
windowResized();


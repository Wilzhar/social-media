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
    var time = formatDate(data.created_at);
    if (userID == data.user_id) {
        li = `<li class="bg-[#7743DB] text-white my-2 p-2 w-3/5 ml-auto mr-0">
            ${data.message}
            <p>${time}</p>
        </li>`
    } else {
        li = `<li class="bg-[#C3ACD0] text-white my-2 p-2 w-3/5 ml-0 mr-auto">
            ${data.message}
            <p>${time}</p>
        </li>`
    }

    ul.innerHTML += li
    window.scrollBy(0, document.body.scrollHeight);
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
    window.scrollBy(0, document.body.scrollHeight);
};


function windowResized() {
    const parent = document.querySelector(".parent");
    document.querySelector(".child").style.width = `${parent.clientWidth - 16}px`;
}

window.addEventListener("resize", windowResized);
windowResized();

document.querySelector('#load-messages').onclick = function (e) {
    loadmoreMessages();
};

function loadmoreMessages() {
    var ul = document.getElementById("chat-log");
    const offset = ul.getElementsByTagName("li").length;
    $.ajax({
        url: '/conversation/messages',
        type: 'GET',
        data: {
            'chat_id': chatID,
            'offset': offset,
        },
        success: function (response) {
            const data = response.messages
            data.map(message => {
                var time = formatDate(message.created_at);
                if (userID == message.user_id) {
                    li = `<li class="bg-[#7743DB] text-white my-2 p-2 w-3/5 ml-auto mr-0">
						${message.text}
						<p>${message.created_at}</p>
					</li>`
                } else {
                    li = `<li class="bg-[#C3ACD0] text-white my-2 p-2 w-3/5 ml-0 mr-auto">
						${message.text}
						<p>${message.created_at}</p>
					</li>`
                }
                ul.innerHTML = li + ul.innerHTML
            })
        },
        error: function (err) {
            console.log(err);
        },
    });
}

function formatDate(string_date) {
    string_date = string_date.trim()
    if (string_date.endsWith("AM")) {
        return string_date.substring(string_date.length - 2) + "a.m."
    } else {
        return string_date.substring(string_date.length - 2) + "p.m."
    }
}

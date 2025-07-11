function typeText(element, text, delay = 20) {
    element.innerHTML = "";
    let i = 0;

    function type() {
        if (i < text.length) {
            element.innerHTML += text.charAt(i);
            i++;
            setTimeout(type, delay);
        }
    }

    type();
}

function appendMessage(sender, text) {
    const chatbox = document.getElementById("chatbox");

    const messageDiv = document.createElement("div");
    messageDiv.className = sender === "user" ? "user-message" : "aura-message";

    const span = document.createElement("span");
    messageDiv.appendChild(span);
    chatbox.appendChild(messageDiv);

    chatbox.scrollTop = chatbox.scrollHeight;

    if (sender === "aura") {
        typeText(span, text, 20);
    } else {
        span.innerText = text;
    }
}

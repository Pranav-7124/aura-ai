function typeText(element, text, delay = 25) {
    element.innerHTML = "";
    let i = 0;

    function typeChar() {
        if (i < text.length) {
            const char = document.createTextNode(text.charAt(i));
            element.appendChild(char);
            i++;
            setTimeout(typeChar, delay);
        }
    }

    typeChar();
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
        typeText(span, text);
    } else {
        span.textContent = text;
    }
}

function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (message === "") return;

    appendMessage("user", message);
    input.value = "";

    fetch("/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => {
        appendMessage("aura", data.response);
    })
    .catch(err => {
        appendMessage("aura", "⚠️ Error connecting to A.U.R.A.");
    });
}

function typeText(element, text, delay = 20) {
    element.textContent = ""; // clear previous content
    let index = 0;

    function type() {
        if (index < text.length) {
            // Add a single character (including spaces!)
            element.textContent += text[index];
            index++;
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
        typeText(span, text); // trigger typing animation
    } else {
        span.textContent = text;
    }
}

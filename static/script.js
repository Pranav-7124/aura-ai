function sendMessage() {
  const userInput = document.getElementById("userInput");
  const message = userInput.value.trim();
  if (!message) return;

  appendMessage(message, "user-message");
  userInput.value = "";

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: message })
  })
  .then(response => response.json())
  .then(data => typeMessage(data.reply, "bot-message"));
}

function appendMessage(text, className) {
  const chatbox = document.getElementById("chatbox");
  const messageDiv = document.createElement("div");
  messageDiv.className = className;
  messageDiv.textContent = text;
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function typeMessage(text, className) {
  const chatbox = document.getElementById("chatbox");
  const messageDiv = document.createElement("div");
  messageDiv.className = className;
  chatbox.appendChild(messageDiv);
  let index = 0;
  const interval = setInterval(() => {
    if (index < text.length) {
      messageDiv.textContent += text.charAt(index);
      index++;
      chatbox.scrollTop = chatbox.scrollHeight;
    } else {
      clearInterval(interval);
    }
  }, 30);
}

document.getElementById('send-btn').addEventListener('click', sendMessage);
document.getElementById('voice-btn').addEventListener('click', startVoiceInput);
document.getElementById('about-btn').addEventListener('click', () => {
  const popup = document.getElementById('about-popup');
  popup.classList.toggle('hidden');
});

function appendMessage(sender, message) {
  const chatBox = document.getElementById('chat-box');
  const msgDiv = document.createElement('div');
  msgDiv.innerHTML = `<strong>${sender}:</strong> <span class="typing-text"></span>`;
  chatBox.appendChild(msgDiv);
  
  const span = msgDiv.querySelector('.typing-text');
  let i = 0;
  const typeEffect = setInterval(() => {
    if (i < message.length) {
      span.innerHTML += message.charAt(i);
      i++;
    } else {
      clearInterval(typeEffect);
    }
  }, 30);

  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById('user-input');
  const message = input.value.trim();
  if (!message) return;
  appendMessage("You", message);
  input.value = "";

  fetch("/get", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ msg: message })
  })
  .then(res => res.json())
  .then(data => appendMessage("A.U.R.A.", data.response));
}

function startVoiceInput() {
  const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
  recognition.lang = 'en-US';
  recognition.start();

  recognition.onresult = function(event) {
    const transcript = event.results[0][0].transcript;
    document.getElementById('user-input').value = transcript;
    sendMessage();
  };
}

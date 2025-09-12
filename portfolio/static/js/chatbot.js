const chatbot = document.getElementById('chatbot');
const CHATBOT_URL = chatbot.dataset.url;
const CSRF_TOKEN = chatbot.dataset.csrf;

const chatbotToggle = document.getElementById('chatbotToggle');
const chatbotClose = document.getElementById('chatbotClose');
const chatForm = document.getElementById('chatForm');
const chatLog = document.getElementById('chatLog');
const chatMessage = document.getElementById('chatMessage');

chatbotToggle.addEventListener('click', () => chatbot.classList.toggle('active'));
chatbotClose.addEventListener('click', () => chatbot.classList.remove('active'));

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const userMessage = chatMessage.value.trim();
    if (!userMessage) return;

    // Show user message
    const userMsgEl = document.createElement('div');
    userMsgEl.classList.add('chat-message', 'user');
    userMsgEl.textContent = userMessage;
    chatLog.appendChild(userMsgEl);
    chatMessage.value = '';
    chatLog.scrollTop = chatLog.scrollHeight;

    // Show bot "typing..." indicator
    const botMsgEl = document.createElement('div');
    botMsgEl.classList.add('chat-message', 'bot');
    botMsgEl.textContent = "Typing...";
    chatLog.appendChild(botMsgEl);
    chatLog.scrollTop = chatLog.scrollHeight;

    // Send message to backend
    const response = await fetch(CHATBOT_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": CSRF_TOKEN
        },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    botMsgEl.textContent = data.reply;
    chatLog.scrollTop = chatLog.scrollHeight;
});

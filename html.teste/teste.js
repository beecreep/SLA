// script.js
document.addEventListener('DOMContentLoaded', () => {
    const chatBox = document.getElementById('chat-box');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');

    // Carregar mensagens do localStorage
    const loadMessages = () => {
        const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
        messages.forEach(addMessageToChatBox);
    };

    // Salvar mensagem no localStorage
    const saveMessage = (message) => {
        const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
        messages.push(message);
        localStorage.setItem('chatMessages', JSON.stringify(messages));
    };

    // Adicionar mensagem ao chat
    const addMessageToChatBox = (message) => {
        const messageElement = document.createElement('p');
        messageElement.textContent = message.text;
        messageElement.classList.add(message.sender === 'principal' ? 'user-message' : 'other-message');
        chatBox.appendChild(messageElement);
        chatBox.scrollTop = chatBox.scrollHeight;
    };

    // Enviar mensagem
    const sendMessage = () => {
        const text = messageInput.value.trim();
        if (text) {
            const userMessage = { text, sender: 'principal' };
            addMessageToChatBox(userMessage);
            saveMessage(userMessage);
            messageInput.value = '';
        }
    };

    // Carregar mensagens ao iniciar
    loadMessages();

    // Eventos
    sendButton.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') sendMessage();
    });
});

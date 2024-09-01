const fileInput = document.getElementById('file');
const textArea = document.getElementById('text-area');
const textInput = document.getElementById('text');
const nome = document.getElementById('name');
let username = ''; // Username padrão

// Função para acionar o input de arquivo
function triggerFileInput() {
  fileInput.click();
}

// Função para lidar com o upload de arquivos
function handleFileUpload() {
  const now = new Date();
  const timestamp = now.toLocaleString();

  if (fileInput.files.length > 0) {
    Array.from(fileInput.files).forEach(file => {
      const fileReader = new FileReader();
      fileReader.onload = function (e) {
        const content = e.target.result;
        const link = document.createElement('a');
        link.href = content;
        link.download = file.name;
        link.textContent = `${username} (${timestamp}): ${file.name}`;
        link.style.display = 'block';
        textArea.appendChild(link);

        // Enviar link de arquivo para o servidor (websocket precisa ser definido)
        // websocket.send(JSON.stringify({
        //   type: 'file',
        //   username,
        //   timestamp,
        //   filename: file.name,
        //   fileurl: content
        // }));

        // Salvar a mensagem de arquivo no localStorage
        saveMessage({ username, timestamp, text: file.name, type: 'file', filecontent: content });
      }
      fileReader.readAsDataURL(file);
    });
    fileInput.value = '';
  }
}

// Função para enviar uma mensagem
function enviar() {
  const now = new Date();
  const timestamp = now.toLocaleString();

  if (textInput.value) {
    const message = {
      username: username,
      timestamp: timestamp,
      text: textInput.value,
      type: 'message'
    };

    addMessageToChat(message);
    saveMessage(message);

    textInput.value = ''; // Limpa o campo de texto após o envio
  }
}

// Função para adicionar uma mensagem ao chat
function addMessageToChat(message) {
  const p = document.createElement('p');
  const span = document.createElement('span');
  span.textContent = ` (${message.timestamp})`;
  span.className = 'timestamp';

  if (message.type === 'file') {
    const link = document.createElement('a');
    link.href = message.filecontent;
    link.download = message.text;
    link.textContent = `${message.username}: ${message.text}`;
    link.style.display = 'block';
    p.appendChild(link);
  } else {
    p.textContent = `${message.username}: ${message.text}`;
    p.appendChild(span);
  }

  textArea.appendChild(p);
  textArea.scrollTop = textArea.scrollHeight;
}

// Função para salvar uma mensagem no localStorage
function saveMessage(message) {
  const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
  messages.push(message);
  localStorage.setItem('chatMessages', JSON.stringify(messages));
}

// Função para carregar mensagens do localStorage
function loadMessages() {
  const messages = JSON.parse(localStorage.getItem('chatMessages')) || [];
  messages.forEach(addMessageToChat);
}

// Função para redefinir o chat
function redefinir() {
  textArea.innerHTML = '';
  textInput.value = '';
  fileInput.value = '';
  localStorage.removeItem('chatMessages');
}

// Código a ser executado quando a janela é carregada
window.onload = function () {
  // Evento para salvar o nome e definir como username
  document.getElementById('usernameForm').addEventListener('submit', function (event) {
    event.preventDefault(); // Evita o comportamento padrão do formulário
    const nameInput = nome.value.trim();
    if (nameInput) {
      username = nameInput; // Define o username como o valor do input
      alert(`Username alterado para: ${username}`);
    }
  });

  // Evento para enviar mensagem ao pressionar Enter
  textInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') {
      enviar(); // Chama a função enviar se Enter for pressionado
      event.preventDefault(); // Evita a quebra de linha ao pressionar Enter
    }
  });

  // Carregar mensagens ao iniciar
  loadMessages();
  document.getElementById('enviar').onclick = enviar;
};

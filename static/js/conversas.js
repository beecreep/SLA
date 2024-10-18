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
        const link = document.createElement('a');
        link.href = e.target.result;
        link.download = file.name;
        link.textContent = `${username} (${timestamp}): ${file.name}`;
        link.style.display = 'block';
        textArea.appendChild(link);

        // Salvar a mensagem de arquivo no localStorage
        saveMessage({ username, timestamp, text: file.name, type: 'file', fileurl: e.target.result });
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
      usuario_id: 123, // Substitua pelo ID do usuário logado
      mensagem: textInput.value
    };

    // Enviar mensagem para o backend via POST
    fetch('/enviar_mensagem', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(message)
    })
    .then(response => response.json())
    .then(data => {
      console.log(data.status); // Exibe a resposta no console
      // Adicionar a mensagem no chat
      addMessageToChat({
        username: username,
        timestamp: timestamp,
        text: message.mensagem
      });
    })
    .catch(error => console.error('Erro ao enviar mensagem:', error));

    textInput.value = ''; // Limpa o campo de texto após o envio
  }
}

// Função para adicionar uma mensagem ao chat
function addMessageToChat(message) {
  const p = document.createElement('p');
  const span = document.createElement('span');
  span.textContent = ` (${message.timestamp})`;
  span.className = 'timestamp';

  p.textContent = `${message.username}: ${message.text}`;
  p.appendChild(span);

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
  fetch('/carregar_mensagens')
    .then(response => response.json())
    .then(mensagens => {
      mensagens.forEach(msg => {
        const message = {
          username: msg[0], // Nome do usuário
          text: msg[1],     // Texto da mensagem
          timestamp: msg[2] // Timestamp
        };
        addMessageToChat(message); // Adiciona a mensagem ao chat
      });
    })
    .catch(error => console.error('Erro ao carregar mensagens:', error));
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

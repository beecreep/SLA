const fileInput = document.getElementById('file');
const textArea = document.getElementById('text-area');
const textInput = document.getElementById('text');

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

        // Enviar link de arquivo para o servidor
        websocket.send(JSON.stringify({
          type: 'file',
          username,
          timestamp,
          filename: file.name,
          fileurl: e.target.result
        }));

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

    if (!textInput) {
        console.error("Elemento de entrada de texto não encontrado");
        return;
    }

  if (textInput.value) {
    const message = {
      username: username,
      timestamp: timestamp,
      text: textInput.value,
      type: 'message'
    };

    addMessageToChat(message);
    saveMessage(message);

    textInput.value = '';
  }
}

// Função para adicionar uma mensagem ao chat
function addMessageToChat(message) {
  const p = document.createElement('p');
  const span = document.createElement('span');
  span.textContent = ` (${message.timestamp})`;
  span.className = 'timestamp';

  // Adiciona o conteúdo da mensagem
  p.textContent = `${message.username}: ${message.text}`;
  p.appendChild(span);

  // Alinhamento das mensagens
  if (message.username === 'Principal') {
    p.className = 'left-align'; // Mensagem do usuário principal à esquerda
  } else {
    p.className = 'right-align'; // Mensagem de outros usuários à direita
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
  document.getElementById('text').value = '';
  document.getElementById('file').value = '';
  localStorage.removeItem('chatMessages');
}
let username = 'Principal'; // Username padrão

window.onload = function() {
    // Função para enviar uma mensagem
    function enviar() {
        const textInput = document.getElementById('text');
        
        if (textInput.value) {
            const now = new Date();
            const timestamp = now.toLocaleString();

            const message = {
                username: username, // Usa o nome definido no formulário
                timestamp: timestamp,
                text: textInput.value,
            };

            addMessageToChat(message);
            saveMessage(message);

            textInput.value = '';  // Limpa o campo de texto após o envio
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

        if (message.username === username) {
            p.className = 'left-align'; // Mensagem do usuário principal à esquerda
        } else {
            p.className = 'right-align'; // Mensagem de outros usuários à direita
        }

        document.getElementById('text-area').appendChild(p);
        document.getElementById('text-area').scrollTop = document.getElementById('text-area').scrollHeight;
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

    // Evento para salvar o nome e definir como username
    document.getElementById('usernameForm').addEventListener('submit', function(event) {
        event.preventDefault(); // Evita o comportamento padrão do formulário
        const nameInput = document.getElementById('name').value.trim();
        if (nameInput) {
            username = nameInput; // Define o username como o valor do input
            alert(`Username alterado para: ${username}`);
        }
    });

    // Evento para enviar mensagem ao pressionar Enter
    document.getElementById('text').addEventListener('keydown', function(event) {
        if (event.key === 'Enter') {
            enviar(); // Chama a função enviar se Enter for pressionado
            event.preventDefault(); // Evita a quebra de linha ao pressionar Enter
        }
    });

    // Carregar mensagens ao iniciar
    loadMessages();
    document.getElementById('enviar').onclick = enviar;
};
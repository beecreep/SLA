const fileInput = document.getElementById('file');
const textArea = document.getElementById('text-area');
const textInput = document.getElementById('text');
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

        // Enviar a mensagem de arquivo para o backend
        enviarArquivo(username, timestamp, file.name, e.target.result);
      }
      fileReader.readAsDataURL(file);
    });
    fileInput.value = '';
  }
}

// Função para enviar uma mensagem
function enviar() {
  const mensagem = document.getElementById('text').value;

  if (mensagem === "") {
    alert("Por favor, preencha o campo.");
    return; // Interrompe a execução da função se o campo estiver vazio
}
  // Enviar a mensagem para o servidor via POST
  fetch('/chat/enviar_mensagem', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ mensagem: mensagem })
})
.then(response => response.json())
.then(data => {
    if (data.status === 'Mensagem enviada com sucesso!') {
        carregarMensagens();  // Atualiza as mensagens no chat
    } else {
        alert(data.message || 'Erro ao enviar a mensagem.');
    }
    })
    .catch(error => {
      console.error("Erro ao enviar mensagem:", error);
      alert("Ocorreu um erro ao enviar a mensagem. Tente novamente.");
  });

  // Limpar o campo de texto
  textInput.value = '';
}

// Função para enviar arquivo para o backend
function enviarArquivo(username, timestamp, fileName, fileData) {
  fetch('/enviar_arquivo', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ username, timestamp, fileName, fileData })
  })
  .then(response => response.json())
  .then(data => {
      // Atualizar a text-area com as mensagens recebidas
      textArea.innerHTML = '';  // Limpar a área de texto
      data.forEach(item => {
          textArea.innerHTML += `<p><strong>${item[0]}:</strong> ${item[1]}</p>`;
      });
  });
}

// Função para carregar mensagens do servidor
function carregarMensagens() {
  fetch('/chat/carregar_mensagens')
      .then(response => response.json())
      .then(data => {
          const chatContainer = document.getElementById('text-area');
          chatContainer.innerHTML = '';  // Limpa o conteúdo

          // Exibe cada mensagem com o timestamp
          data.forEach(item => {
              const messageElement = document.createElement('p');
              messageElement.innerHTML = `<strong>${item.nome}:</strong> ${item.texto} <span>(${item.timestamp})</span>`;
              chatContainer.appendChild(messageElement);
          });
      })
      .catch(error => console.error('Erro ao carregar as mensagens:', error));
}

document.addEventListener('DOMContentLoaded', carregarMensagens);

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

// Função para redefinir o chat
function redefinir() {
  textArea.innerHTML = '';
  textInput.value = '';
  fileInput.value = '';
}

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

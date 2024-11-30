const fileInput = document.getElementById('file');
const textArea = document.getElementById('text-area');
const textInput = document.getElementById('text');
let username = ''; // Username padrão

// Função para acionar o input de arquivo
function triggerFileInput() {
  fileInput.click();
}

// Função para enviar uma mensagem
async  function enviar() {
  const form = document.querySelector('form');
  const formData = new FormData(form); // Captura todos os campos do formulário automaticamente.
 
  if (mensagem) {
    formData.append('mensagem', mensagem);
  }

  if (arquivo) {
    formData.append('arquivo', arquivo);
  }

      // Verifica se ao menos mensagem ou arquivo foi fornecido
      if (!formData.get('mensagem') && !formData.get('arquivo')) {
        alert('Por favor, insira uma mensagem ou selecione um arquivo.');
        return;
    }

  // Enviar a mensagem para o servidor via POST
  try {
    // Envia os dados para o backend
    const response = await fetch('/chat/enviar_mensagem', {
        method: 'POST',
        body: formData,
    });
    
    const result = await response.json();

    if (result.status === 'Mensagem enviada com sucesso!') {
        carregarMensagens();  // Atualiza o chat
    } 
    else {
        alert(result.message || 'Erro ao enviar a mensagem.');
    }
} 
catch (error) {
  console.error('Erro ao enviar a mensagem:', error);
  alert('Ocorreu um erro ao enviar a mensagem. Tente novamente.');
  return; // Interrompe a execução
}
  // Limpar o campo de texto
  form.reset();

};

// Função para carregar mensagens do servidor
function carregarMensagens() {
  fetch('/chat/carregar_mensagens')
      .then(response => response.json())
      .then(mensagens => {
          textArea.innerHTML = '';  // Limpa o conteúdo

          // Exibe cada mensagem com o timestamp
          mensagens.forEach(addMessageToChat);
      })
      .catch(error => console.error('Erro ao carregar as mensagens:', error));
}

document.addEventListener('DOMContentLoaded', carregarMensagens);

// Função para adicionar uma mensagem ao chat
function addMessageToChat(message) {
  const p = document.createElement('p');

      // Adiciona o nome do usuário
      const spanUsername = document.createElement('span');
      spanUsername.textContent = `${message.nome}: `;
      spanUsername.style.fontWeight = 'bold';
      p.appendChild(spanUsername);
  

  if (message.mensagem) {
    const spanMensagem = document.createElement('span');
    spanMensagem.textContent = `${message.mensagem} `;
    p.appendChild(spanMensagem);
}

if (message.arquivo_url) {
  // Exibe o arquivo como link para download
  const link = document.createElement('a');
  link.href = message.arquivo_url;
  link.textContent = `${message.nome} enviou um arquivo (${message.extensao.toUpperCase()})`;
  link.target = '_blank'; // Abre o arquivo em uma nova aba
  link.style.marginLeft = '5px';
  p.appendChild(link);
} 

   // Adiciona o timestamp
   const spanTimestamp = document.createElement('span');
   spanTimestamp.textContent = ` (${message.timestamp})`;
   spanTimestamp.className = 'timestamp';
   p.appendChild(spanTimestamp);

  
  // Adiciona o parágrafo ao chat e rola a visualização para a última mensagem
  textArea.appendChild(p);
  textArea.scrollTop = textArea.scrollHeight;
}

setInterval(carregarMensagens, 3000);

// Evento para enviar mensagem ao pressionar Enter
textInput.addEventListener('keydown', function (event) {
  if (event.key === 'Enter') {
    enviar(); // Chama a função enviar se Enter for pressionado
    event.preventDefault(); // Evita a quebra de linha ao pressionar Enter
  }
});

// Carregar mensagens ao iniciar
carregarMensagens();

document.getElementById('enviar').onclick = enviar;

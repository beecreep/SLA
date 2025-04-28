Para encaminhar o conteúdo da tag `<main>` de "professor.html" para a seção de atividades em "aluno.html" usando `localStorage`, podemos armazenar as informações da atividade quando o professor submete o formulário, e depois recuperá-las na página do aluno. Aqui está um exemplo de como implementar essa lógica:

1. **No arquivo "professor.html"**, você precisa salvar o conteúdo ao enviar a atividade:

```javascript
// Função que envia a atividade e salva no localStorage
function uploadFile() {
    const titulo = document.querySelector('.titulo').value;
    const descricao = document.querySelector('#descriçao-atividade').value;
    const dueDate = document.getElementById('due-date').value;

    if (titulo && descricao && dueDate) {
        // Cria um objeto da atividade
        const atividade = {
            titulo: titulo,
            descricao: descricao,
            data: dueDate
        };

        // Salva a atividade no localStorage
        localStorage.setItem('atividade', JSON.stringify(atividade));
        alert('Atividade enviada com sucesso!');
    } else {
        alert('Preencha todos os campos.');
    }
}
```

2. **No arquivo "aluno.html"**, você precisa recuperar e exibir as informações da atividade armazenada no `localStorage`:

```javascript
// Função que carrega a atividade no aluno.html
function carregarAtividade() {
    const atividade = JSON.parse(localStorage.getItem('atividade'));

    if (atividade) {
        // Atualiza a seção de atividades com o conteúdo
        const atividadesSection = document.getElementById('Atividades');
        atividadesSection.innerHTML = `
            <h2>${atividade.titulo}</h2>
            <p>${atividade.descricao}</p>
            <p>Data de entrega: ${atividade.data}</p>
        `;
        atividadesSection.style.display = 'block';
    } else {
        alert('Nenhuma atividade encontrada.');
    }
}

// Chama a função quando a página for carregada
window.onload = carregarAtividade;
```

3. **Como chamar a função no "aluno.html"**:

Adicione o código no `script` da página "aluno.html" para chamar a função `carregarAtividade` ao carregar a página.

Agora, quando o professor enviar uma atividade, ela será salva no `localStorage` e recuperada automaticamente quando o aluno acessar a página de atividades.
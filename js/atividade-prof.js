const lixeira = document.getElementById('lixeira');
const textarea = document.querySelectorAll('.file-description');
const fileInput = document.getElementById('file-upload');
let uploudform = document.getElementById('upload-form')
const fileList = document.getElementById('file-list');

function uploadFile() {
    const titulo = document.querySelector('.titulo').value;
    const descricao = document.querySelector('#descriçao-atividade').value;
    const dueDate = document.getElementById('due-date').value;

    if (titulo && descricao && dueDate) {
        // Cria uma string HTML estilizada
        const atividadeHTML = `
            <div style="border: 2px solid black; padding: 10px; margin: 10px; border-radius: 8px;">
                <h2 style="font-size: 1.5em; color: blue;">${titulo}</h2>
                <p style="font-size: 1.2em;">${descricao}</p>
                <p style="font-weight: bold;">Data de entrega: ${dueDate}</p>
            </div>
        `;

        // Salva a estrutura HTML da atividade no localStorage
        localStorage.setItem('atividadeHTML', atividadeHTML);
        alert('Atividade enviada com sucesso!');
    } else {
        alert('Preencha todos os campos.');
    }
}
textarea.forEach((element) => {
    element.addEventListener('input', function () {
        this.style.height = 'auto'; // Redefine a altura para calcular a nova altura
        this.style.height = this.scrollHeight + 'px'; // Define a altura com base no scrollHeight
    });
});

const loginform = document.getElementById('login-Form')
const login = document.getElementById('login')

loginform.addEventListener('submit', async (event) => {
event.preventDefault();

const formData = new FormData(event.target);
const data = Object.fromEntries(formData.entries());

try {
const response = await fetch('/cadastrar/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
});

const result = await response.json();

if (result.status === 'success') {
    window.location.href = result.redirect_url;
} else {
    alert('Login failed');
}
} catch (error) {
console.error('Erro na requisição de login:', error);
alert('Erro ao fazer login');
}
});

// Função para cadastrar novo usuário
async function cadastrar() {
    const nome = document.querySelector('input[placeholder="Nome"]').value;
    const email = document.querySelector('input[placeholder="email"]').value;
    const senha = document.querySelector('input[placeholder="senha"]').value;
    const confirmasenha = document.querySelector('input[placeholder="confirme sua senha "]').value;
    const turma = document.querySelector('select[name="turma"]').value;
    const numero = document.querySelector('input[placeholder="(xx)xxxxx-xxxx"]').value;
    const role = document.querySelector('input[name="role"]:checked').value;

    // Verifica se a senha e a confirmação de senha correspondem
    if (senha !== confirmasenha) {
        alert('As senhas não conferem!');
        return;
    }

    // Prepara os dados para enviar ao servidor
    const dadosCadastro = { nome, email, senha, turma, numero, role };

    try {
        // Envia os dados para a rota de cadastro
        const response = await fetch('/cadastrar/cadastrar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dadosCadastro)
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.status);  // Exibe a mensagem de sucesso
            login.style.display = 'flex';
            document.getElementById('main-content').style.display = 'none';
              // Redireciona após cadastro
        } else {
            alert(data.error || 'Erro ao cadastrar usuário.');
        }
    } catch (error) {
        console.error('Erro:', error);
        alert('Erro ao fazer cadastro. Tente novamente.');
    }
}

document.getElementById('cadastrar-btn').addEventListener('click', function () {
    login.style.display = 'none';
    document.getElementById('main-content').style.display = 'flex';
});
document.getElementById('entrar').addEventListener('click', function () {
    document.getElementById('main-content').style.display = 'none';
    login.style.display = 'flex';
});

document.getElementById('continuar').addEventListener('click', function (event) {
    const emailInput = document.getElementById('email').value;

    // Regex para validar emails com domínios conhecidos (gmail, yahoo, etec, etc.)
    const emailRegex = /^[^\s@]+@[^\s@]+\.(gmail|yahoo|etec|com|org|net)$/i;

    if (!emailRegex.test(emailInput)) {
        alert('Por favor, insira um email válido (ex: @gmail, @yahoo, @etec).');
        event.preventDefault(); // Impede qualquer ação subsequente ao clique
        return;
    }
});
// Supondo que você já tenha a função de login configurada com fetch

document.getElementById('numero').addEventListener('input', function (e) {
let input = e.target.value.replace(/\D/g, '');  // Remove caracteres não numéricos
if (input.length > 0) input = `(${input.slice(0, 2)})${input.slice(2)}`;
if (input.length > 9) input = `${input.slice(0, 9)}-${input.slice(9, 13)}`;
e.target.value = input;
});

// Função para cadastrar novo u
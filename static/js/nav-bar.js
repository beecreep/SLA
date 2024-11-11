
let atividadesbtn = document.getElementById('Atividades-btn');
let mainContentElements = document.getElementsByClassName('main-content');
let conversasbtn = document.getElementById('conversas-btn');
let materiasbtn = document.getElementById('materias-btn')
let materias1 = document.getElementById('materias1');
let atividades = document.getElementById('Atividades');
const perfilbtn = document.getElementById('perfil-btn');
const perfil = document.getElementById('perfil');
const cronogramasbtn = document.getElementById('Cronogramas-btn');
const cronogramas = document.getElementById('CRONOGRAMAS');
const image = document.querySelectorAll('.imagem');
const foto = document.getElementById('foto');


atividadesbtn.addEventListener("click", () => {
    // Obter todos os elementos com a classe 'main-content'

    materias1.style.display = 'none';
    atividades.style.display = 'grid';
    perfil.style.display = 'none';
    cronogramas.style.display = 'none'

});

cronogramasbtn.addEventListener("click", () => {
    // Obter todos os elementos com a classe 'main-content'
    
    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    cronogramas.style.display = 'flex';

});
perfilbtn.addEventListener("click", () => {

    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'grid';
    cronogramas.style.display = 'none';

});
conversasbtn.addEventListener("click", () => {
    // Iterar sobre todos os elementos e definir display para 'none'
    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    cronogramas.style.display = 'none'
    // Definir display para 'grid' no elemento com id 'materias1'

});

materiasbtn.addEventListener("click", () => {
   
    materias1.style.display = 'grid';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    cronogramas.style.display = 'none'

});
// Função para alternar a exibição da navbar
function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('section');
    navbar.classList.toggle('show');
    mainContent.classList.toggle('shifted');
}

foto.addEventListener("change", () => {
    if (foto.files.length > 0) {
        const newImageSrc = URL.createObjectURL(foto.files[0]);
        image.forEach(img => {
            img.src = newImageSrc;
        });
    }
})
document.getElementById('image2').addEventListener("click", () => {
    foto.click();
});

function toggleTheme() {
    const body = document.body;
    const button = document.querySelector('.button-theme-toggle');
    body.classList.toggle('dark-mode');

    if (body.classList.contains('dark-mode')) {
        button.innerHTML = '&#9789;'; // Lua
    } else {
        button.innerHTML = '&#9788;'; // Sol
    }
}

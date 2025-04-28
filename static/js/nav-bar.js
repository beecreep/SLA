
let materiasbtn = document.getElementById('materias-btn')
let materias1 = document.getElementById('materias1');
const perfilbtn = document.getElementById('perfil-btn');
const perfil = document.getElementById('perfil');
const cronogramasbtn = document.getElementById('Cronogramas-btn');

perfilbtn.addEventListener("click", () => {

    materias1.style.display = 'none';
    perfil.style.display = 'grid';

});

materiasbtn.addEventListener("click", () => {
   
    materias1.style.display = 'grid';
    perfil.style.display = 'none';

});
// Função para alternar a exibição da navbar
function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('section');
    navbar.classList.toggle('show');
    mainContent.classList.toggle('shifted');
}

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

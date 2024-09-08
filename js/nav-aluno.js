
let atividadesbtn = document.getElementById('Atividades-btn');
let mainContentElements = document.getElementsByClassName('main-content');
let conversasbtn = document.getElementById('conversas-btn');
let materiasbtn = document.getElementById('materias-btn')
let materias1 = document.getElementById('materias1');
let atividades = document.getElementById('Atividades');
let perfilbtn = document.getElementById('perfil-btn');
let perfil = document.getElementById('perfil');
let cronogramasbtn = document.getElementById('Cronogramas-btn');
let cronogramas = document.getElementById('CRONOGRAMAS');


atividadesbtn.addEventListener("click", () => {
    // Obter todos os elementos com a classe 'main-content'
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }

    materias1.style.display = 'none';
    atividades.style.display = 'grid';
    perfil.style.display = 'none';
    cronogramas.style.display = 'none'

});
cronogramasbtn.addEventListener("click", () => {
    // Obter todos os elementos com a classe 'main-content'
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }

    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    cronogramas.style.display = 'flex';

});
perfilbtn.addEventListener("click", () => {

    for (let element of mainContentElements) {
        element.style.display = 'none';
    }

    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'grid';
    cronogramas.style.display = 'none';

});
conversasbtn.addEventListener("click", () => {
    // Iterar sobre todos os elementos e definir display para 'none'
    for (let element of mainContentElements) {
        element.style.display = 'flex';
    }
    materias1.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    cronogramas.style.display = 'none'
    // Definir display para 'grid' no elemento com id 'materias1'

});
 materiasbtn.addEventListener("click", () => {
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }
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

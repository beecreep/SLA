
let atividadesbtn = document.getElementById('Atividades-btn');
        let mainContentElements = document.getElementsByClassName('main-content');
        let conversasbtn = document.getElementById('conversas-btn');
        let materiasbtn = document.getElementById('materias-btn')
        let materias = document.getElementById('materias');
        let atividades = document.getElementById('Atividades');
        let perfilbtn = document.getElementById('perfil-btn');
        let perfil = document.getElementById('perfil');
        
        
        atividadesbtn.addEventListener("click", () => {
    // Obter todos os elementos com a classe 'main-content'
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }

    materias.style.display = 'none';
    atividades.style.display = 'grid';
    perfil.style.display = 'none';

});
perfilbtn.addEventListener("click", () => {
  
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }

    materias.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'grid';

});
conversasbtn.addEventListener("click", () => {
    // Iterar sobre todos os elementos e definir display para 'none'
    for (let element of mainContentElements) {
        element.style.display = 'flex';
    }
    materias.style.display = 'none';
    atividades.style.display = 'none';
    perfil.style.display = 'none';
    // Definir display para 'grid' no elemento com id 'materias'

});
materiasbtn.addEventListener("click", () => {
    for (let element of mainContentElements) {
        element.style.display = 'none';
    }
    materias.style.display = 'grid';
    atividades.style.display = 'none';
    perfil.style.display = 'none';

});
   // Função para alternar a exibição da navbar
   function toggleNavbar() {
    const navbar = document.querySelector('.navbar');
    const mainContent = document.querySelector('section');
    navbar.classList.toggle('show');
    mainContent.classList.toggle('shifted');
}  

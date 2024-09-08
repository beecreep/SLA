keys.forEach(key => {
    key.addEventListener('click', function() {
        // Obtém o ID do conteúdo a ser mostrado a partir do atributo 'data-target'
        const target = document.getElementById(this.getAttribute('data-target'));
        
        // Alterna o display do conteúdo relacionado
        target.style.display = (target.style.display === 'block') ? 'none' : 'block';
    });
});
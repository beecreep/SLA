Criar uma nav-bar responsiva envolve o uso de flexbox para organizar os itens e de media queries para ajustar o layout conforme a largura da tela muda. Exemplo:

### HTML

```html
<header>
    <nav class="navbar">
        <div class="logo">
            <a href="#">Meu Projeto</a>
        </div>
        <ul class="nav-links">
            <li><a href="#home">Início</a></li>
            <li><a href="#sobre">Sobre</a></li>
            <li><a href="#projeto">Projeto</a></li>
            <li><a href="#contato">Contato</a></li>
        </ul>
        <div class="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </nav>
</header>
```

### CSS

```css
/* Estilos Gerais */
body {
    margin: 0;
    font-family: Arial, sans-serif;
}

header {
    background-color: #007BFF;
    color: #fff;
    padding: 10px 20px;
}

.navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.logo a {
    color: #fff;
    text-decoration: none;
    font-size: 1.5em;
    font-weight: bold;
}

.nav-links {
    display: flex;
    list-style: none;
    margin: 0;
    padding: 0;
}

.nav-links li {
    margin-left: 20px;
}

.nav-links a {
    color: #fff;
    text-decoration: none;
    font-size: 1.2em;
    transition: color 0.3s ease;
}

.nav-links a:hover {
    color: #ffcc00;
}

.hamburger {
    display: none;
    flex-direction: column;
    cursor: pointer;
}

.hamburger span {
    height: 3px;
    width: 25px;
    background-color: #fff;
    margin: 4px 0;
    border-radius: 2px;
    transition: 0.4s;
}

/* Media Query para telas menores */
@media (max-width: 768px) {
    .nav-links {
        display: none;
        flex-direction: column;
        width: 100%;
        position: absolute;
        top: 60px;
        left: 0;
        background-color: #007BFF;
    }

    .nav-links li {
        margin: 15px 0;
        text-align: center;
    }

    .hamburger {
        display: flex;
    }

    .nav-links.active {
        display: flex;
    }
}
```

### JavaScript

Para controlar a exibição do menu em telas menores, você pode adicionar o seguinte script:

```javascript
document.querySelector(".hamburger").addEventListener("click", function() {
    document.querySelector(".nav-links").classList.toggle("active");
});
```

### Explicação

- **Flexbox:** A nav-bar é inicialmente organizada usando flexbox, com os itens de navegação alinhados à direita e o logotipo à esquerda.
  
- **Hamburger Menu:** O menu "hamburger" (ícone com três linhas) aparece apenas em telas menores (abaixo de 768px). Quando clicado, ele exibe ou esconde o menu de navegação.

- **Media Query:** A media query reorganiza a nav-bar em telas menores. O menu se transforma em um menu "hamburger", e os links são ocultados inicialmente até que o menu seja clicado.

- **Animação e Transições:** Pequenas transições são adicionadas para suavizar o comportamento do menu, como a mudança de cor nos links e a transformação do ícone "hamburger".

Este exemplo básico pode ser expandido e estilizado de acordo com as necessidades do seu projeto, garantindo que a navegação funcione bem em dispositivos móveis e desktops.
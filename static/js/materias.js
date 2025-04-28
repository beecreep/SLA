
const curiosidades = [
   "Sabia que o Raspberry Pi foi lançado em 2012 para promover a educação em computação?",
    "O ESP32 é conhecido por sua alta eficiência energética e suporte a Wi-Fi e Bluetooth simultaneamente!",
    "Microcontroladores são usados em muitos dispositivos do cotidiano, como carros, eletrodomésticos e brinquedos.",
    "O Arduino é uma plataforma de hardware livre amplamente usada para criar protótipos de eletrônica e robótica.",
    "O primeiro computador eletrônico, ENIAC, foi desenvolvido na década de 1940 e ocupava uma sala inteira!",
    "O Raspberry Pi 4 tem capacidade de rodar sistemas operacionais como o Linux e até versões leves do Windows.",
    "O ESP32 possui uma CPU dual-core, o que permite que ele execute tarefas complexas em tempo real.",
    "Microcontroladores podem ser encontrados em dispositivos médicos, como marcapassos e ventiladores.",
    "Sabia que o Arduino pode ser programado usando a linguagem C++? É uma ótima ferramenta para aprender programação.",
    "Os sensores de temperatura e umidade são componentes comuns em projetos com ESP32 e Raspberry Pi.",
    "O Raspberry Pi é pequeno, mas poderoso o suficiente para ser usado como servidor web!",
    "O Arduino tem uma vasta comunidade de entusiastas, o que facilita encontrar tutoriais e bibliotecas de código prontos.",
    "O ESP32 é amplamente utilizado em projetos de automação residencial e IoT (Internet das Coisas).",
    "O Raspberry Pi pode ser usado como um media center, transformando qualquer TV em uma smart TV.",
    "Sabia que o primeiro microcontrolador foi criado em 1971 pela Intel e era chamado de 4004?",
    "Os sistemas embarcados, como os usados no ESP32 e Raspberry Pi, estão em quase todos os dispositivos eletrônicos modernos.",
    "O Raspberry Pi pode ser usado em projetos de inteligência artificial, graças ao suporte a bibliotecas de aprendizado de máquina.",
    "O Arduino Nano é uma versão compacta do Arduino, ideal para projetos que precisam de espaço reduzido.",
    "O ESP32 suporta criptografia e é uma ótima escolha para projetos que precisam de segurança em comunicações de dados.",
    "O Raspberry Pi também pode ser usado como um controlador para impressoras 3D!"
];

function mostrarCuriosidade() {
    const randomCuriosidade = curiosidades[Math.floor(Math.random() * curiosidades.length)];
    document.getElementById('banner-content').textContent = randomCuriosidade;
}
// Alterar curiosidade a cada 10 segundos
setInterval(mostrarCuriosidade, 10000);

// Exibir a primeira curiosidade ao carregar a página
window.onload = mostrarCuriosidade;

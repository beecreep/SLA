const prevWeekButton = document.getElementById('prev-week');
const nextWeekButton = document.getElementById('next-week');
const currentWeekSpan = document.getElementById('current-week');

let currentWeek = 1; // Exemplo de controle simples de semanas

prevWeekButton.addEventListener('click', () => {
    currentWeek--;
    updateWeekDisplay();
});

nextWeekButton.addEventListener('click', () => {
    currentWeek++;
    updateWeekDisplay();
});

function updateWeekDisplay() {
    currentWeekSpan.textContent = `Semana ${currentWeek}`;
    // Aqui você pode implementar a lógica de exibição dinâmica do cronograma
}

// Função para gerar um calendário mensal
function generateCalendar(month, year) {
    const calendarDiv = document.getElementById('calendar');
    calendarDiv.innerHTML = ''; // Limpa o calendário anterior

    const daysInMonth = new Date(year, month + 1, 0).getDate();
    for (let day = 1; day <= daysInMonth; day++) {
        const dayDiv = document.createElement('div');
        dayDiv.textContent = day;
        calendarDiv.appendChild(dayDiv);
    }
}

// Exemplo de uso
const today = new Date();
generateCalendar(today.getMonth(), today.getFullYear());
// script.js

document.addEventListener('DOMContentLoaded', () => {
    const prevMonthButton = document.getElementById('prev-month');
    const nextMonthButton = document.getElementById('next-month');
    const monthYearSpan = document.getElementById('month-year');
    const calendarDiv = document.getElementById('calendar');

    let currentDate = new Date();

    // Definição de feriados fixos (aplicável a todos os anos)
    const fixedHolidays = {
        '12-25': 'Natal',
        '01-01': 'Ano Novo',
        '04-21': 'Tiradentes',
        '09-07': 'Independência do Brasil',
        '05-01': 'Dia do Trabalhador',
        '11-02': 'dia de finados',
        '11-15' : 'Proclamação da republica '
    };

    // Função para calcular feriados móveis (Páscoa, Carnaval, etc.)
    function calculateVariableHolidays(year) {
        const holidays = {};

        // Exemplo: Adicionar Páscoa (calculo baseado no algoritmo de computus)
        const easter = calculateEaster(year);
        holidays[easter.toISOString().split('T')[0]] = 'Páscoa';

        // Adicione feriados móveis conforme necessário, ex: Carnaval 47 dias antes da Páscoa
        const carnival = new Date(easter);
        carnival.setDate(easter.getDate() - 47);
        holidays[carnival.toISOString().split('T')[0]] = 'Carnaval';

        return holidays;
    }

    // Algoritmo para calcular a data da Páscoa (exemplo de cálculo)
    function calculateEaster(year) {
        const f = Math.floor;
        const G = year % 19;
        const C = f(year / 100);
        const H = (C - f(C / 4) - f((8 * C + 13) / 25) + 19 * G + 15) % 30;
        const I = H - f(H / 28) * (1 - f(29 / (H + 1)) * f((21 - G) / 11));
        const J = (year + f(year / 4) + I + 2 - C + f(C / 4)) % 7;
        const L = I - J;
        const month = 3 + f((L + 40) / 44);
        const day = L + 28 - 31 * f(month / 4);
        return new Date(year, month - 1, day);
    }

    // Função para gerar o calendário
    function generateCalendar(date) {
        calendarDiv.innerHTML = ''; // Limpa o calendário anterior

        // Adiciona os nomes dos dias da semana
        const dayNames = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb'];
        dayNames.forEach(day => {
            const dayNameDiv = document.createElement('div');
            dayNameDiv.classList.add('day-name');
            dayNameDiv.textContent = day;
            calendarDiv.appendChild(dayNameDiv);
        });

        const year = date.getFullYear();
        const month = date.getMonth();

        // Atualiza o título do mês e ano
        const monthNames = [
            'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
            'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
        ];
        monthYearSpan.textContent = `${monthNames[month]} ${year}`;

        // Combina feriados fixos e móveis
        const variableHolidays = calculateVariableHolidays(year);
        const holidays = { ...fixedHolidays, ...variableHolidays };

        // Primeiro dia do mês
        const firstDay = new Date(year, month, 1);
        const startingDay = firstDay.getDay();

        // Número de dias no mês
        const daysInMonth = new Date(year, month + 1, 0).getDate();

        // Preenche os dias antes do primeiro dia do mês
        for (let i = 0; i < startingDay; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.classList.add('day');
            calendarDiv.appendChild(emptyDiv);
        }

        // Preenche os dias do mês
        for (let day = 1; day <= daysInMonth; day++) {
            const dayDiv = document.createElement('div');
            dayDiv.classList.add('day');
            const fullDate = `${year}-${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;

            // Verifica se é o dia atual
            const today = new Date();
            if (day === today.getDate() && month === today.getMonth() && year === today.getFullYear()) {
                dayDiv.classList.add('today');
            }

            // Verifica se é feriado (fixo ou móvel)
            const holidayKey = `${String(month + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
            if (holidays[fullDate] || holidays[holidayKey]) {
                dayDiv.classList.add('holiday');
                const marker = document.createElement('div');
                marker.classList.add('holiday-marker');
                dayDiv.appendChild(marker);

                // Opcional: mostrar o nome do feriado ao passar o mouse
                dayDiv.title = holidays[fullDate] || holidays[holidayKey];
            }

            dayDiv.textContent = day;
            calendarDiv.appendChild(dayDiv);
        }

        // Preenche os espaços após o último dia do mês para completar a semana
        const totalCells = startingDay + daysInMonth;
        const remainingCells = totalCells % 7 === 0 ? 0 : 7 - (totalCells % 7);
        for (let i = 0; i < remainingCells; i++) {
            const emptyDiv = document.createElement('div');
            emptyDiv.classList.add('day');
            calendarDiv.appendChild(emptyDiv);
        }
    }

    // Funções para navegar entre os meses
    function prevMonth() {
        currentDate.setMonth(currentDate.getMonth() - 1);
        generateCalendar(currentDate);
    }

    function nextMonth() {
        currentDate.setMonth(currentDate.getMonth() + 1);
        generateCalendar(currentDate);
    }

    prevMonthButton.addEventListener('click', prevMonth);
    nextMonthButton.addEventListener('click', nextMonth);

    // Inicializa o calendário com a data atual
    generateCalendar(currentDate);
});



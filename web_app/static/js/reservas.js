const token = localStorage.getItem('token');
if (!token) {
    window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
}

// Todas as reservas do cliente, sem filtro
let TODAS_AS_RESERVAS = [];

async function carregarReservas() {
    const resultado = await buscarReservas();


    if (!resultado.ok) {
            window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
            return;
        }

    TODAS_AS_RESERVAS = resultado.dados;
    desenharReservas(TODAS_AS_RESERVAS);
}

// criar funcao para criar cabeçalho da tabela

function criarCabecalhoTabela() {
    const thead = document.createElement('thead');
    const tr = document.createElement('tr');

    const colunas = ['Matrícula', 'Marca', 'Modelo', 'Data Início', 'Data Fim', 'Valor Total', 'Estado', '', ''];

    colunas.forEach(coluna => {
        const th = document.createElement('th');
        th.textContent = coluna;
        tr.appendChild(th);
    });

    thead.appendChild(tr);
    return thead;
}

// criar funcao para listar reservas

function criarLinhaReserva(reserva) {
    const tr = document.createElement('tr');

    const valores = [
        reserva.veiculo.matricula,
        reserva.veiculo.marca,
        reserva.veiculo.modelo,
        reserva.data_inicio,
        reserva.data_fim,
        `${reserva.valor_total}€`,
        reserva.estado
    ];

    valores.forEach(valor => {
        const td = document.createElement('td');
        td.textContent = valor;
        tr.appendChild(td);
    });

    const tdAlterar = document.createElement('td');
    const tdCancelar = document.createElement('td');
    tr.appendChild(tdAlterar);
    tr.appendChild(tdCancelar);

    if (reserva.estado === 'Reservada') {
        const botaoAlterar = document.createElement('button');
        botaoAlterar.textContent = 'Alterar';
        botaoAlterar.className = 'botao-principal';
        tdAlterar.appendChild(botaoAlterar);

        const inputInicio = document.createElement('input');
        inputInicio.type = 'date';
        inputInicio.value = reserva.data_inicio;
        inputInicio.hidden = true;
        tdAlterar.appendChild(inputInicio);

        const inputFim = document.createElement('input');
        inputFim.type = 'date';
        inputFim.value = reserva.data_fim;
        inputFim.hidden = true;
        tdAlterar.appendChild(inputFim);

        const botaoGuardar = document.createElement('button');
        botaoGuardar.textContent = 'Guardar';
        botaoGuardar.className = 'botao-principal';
        botaoGuardar.hidden = true;
        tdAlterar.appendChild(botaoGuardar);

        // Botão de Cancelar reserva
        const botaoCancelar = document.createElement('button');
        botaoCancelar.textContent = 'Cancelar';
        botaoCancelar.className = 'botao-principal';
        tdCancelar.appendChild(botaoCancelar);

        botaoCancelar.addEventListener('click', async () => {
            const resultado = await cancelarReserva(reserva.id)
            
            if (!resultado.ok) {
                alert(resultado.dados.erro);
            } else {
                carregarReservas();
            }
        });

        botaoAlterar.addEventListener('click', () => {
            botaoCancelar.hidden = true;
            botaoAlterar.hidden = true;
            inputInicio.hidden = false;
            inputFim.hidden = false;
            botaoGuardar.hidden = false;
        });

        botaoGuardar.addEventListener('click', async () => {
            const resultado = await alterarReserva(reserva.id, inputInicio.value, inputFim.value);

            if(!resultado.ok) {
                alert(resultado.dados.erro);
            } else {
                carregarReservas();
            }
        });
    }

    if (reserva.estado === 'Ativa') {
        const botaoAlterar = document. createElement('button');
        botaoAlterar.textContent = 'Alterar';
        botaoAlterar.className = 'botao-principal';
        tdAlterar.appendChild(botaoAlterar);

        const inputFim = document.createElement('input');
        inputFim.type = 'date';
        inputFim.value = reserva.data_fim;
        inputFim.hidden = true;
        tdAlterar.appendChild(inputFim);

        const botaoGuardar = document.createElement('button');
        botaoGuardar.textContent = 'Guardar';
        botaoGuardar.className = 'botao-principal';
        botaoGuardar.hidden = true;
        tdAlterar.appendChild(botaoGuardar);

        botaoAlterar.addEventListener('click', () => {
            botaoAlterar.hidden = true;
            inputFim.hidden = false;
            botaoGuardar.hidden = false;
        });

        botaoGuardar.addEventListener('click', async () => {
            const resultado = await alterarReserva(reserva.id, null, inputFim.value);

            if (!resultado.ok) {
                alert(resultado.dados.erro);
            } else {
                carregarReservas();
            }
        });
    }

    return tr;
}

function desenharReservas(reservas) {
    const container = document.getElementById('lista-reservas');
    container.innerHTML = '';

    const table = document.createElement('table');
    table.appendChild(criarCabecalhoTabela());

    const tbody = document.createElement('tbody');
    reservas.forEach(reserva => {
        tbody.appendChild(criarLinhaReserva(reserva));
    });
    table.appendChild(tbody);
    
    container.appendChild(table);
}

carregarReservas();
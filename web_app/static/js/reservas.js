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
    aplicarFiltroReservas();
}

// Select de filtro por estado, acima da tabela
function montarFiltroEstado() {
    const opcoes = [
        { valor: '', texto: '— Todos —' },
        { valor: 'Reservada', texto: 'Reservada' },
        { valor: 'Ativa', texto: 'Ativa' },
        { valor: 'Concluída', texto: 'Concluída' },
        { valor: 'Cancelada', texto: 'Cancelada' }
    ];

    const campo = criarCampoSelect('filtro-estado', 'Estado:', opcoes);
    document.getElementById('filtro-reservas').appendChild(campo);
    document.getElementById('filtro-estado').addEventListener('change', aplicarFiltroReservas);
}

// Por o filtro a funcionar
function aplicarFiltroReservas() {
    const estado = document.getElementById('filtro-estado').value;

    if(!estado) {
        desenharReservas(TODAS_AS_RESERVAS);
        return;
    }

    const filtradas = TODAS_AS_RESERVAS.filter(reserva => reserva.estado === estado);
    desenharReservas(filtradas);
}

// Colunas da tabela: título, valor em bruto e formatação opcional
const COLUNAS = [
    { titulo: 'Matrícula', valor: reserva => reserva.veiculo.matricula },
    { titulo: 'Marca', valor: reserva => reserva.veiculo.marca },
    { titulo: 'Modelo', valor: reserva => reserva.veiculo.modelo },
    { titulo: 'Data Início', valor: reserva => reserva.data_inicio },
    { titulo: 'Data Fim', valor: reserva => reserva.data_fim },
    { titulo: 'Valor Total', valor: reserva => reserva.valor_total, formatar: valor => `${valor}€` },
    { titulo: 'Estado', valor: reserva => reserva.estado }
];

// criar funcao para criar cabeçalho da tabela
function criarCabecalhoTabela() {
    const thead = document.createElement('thead');
    const tr = document.createElement('tr');

    COLUNAS.forEach(coluna => {
        const th = document.createElement('th');
        th.textContent = coluna.titulo;
        tr.appendChild(th);
    });

    // Colunas dos botões Alterar e Cancelar
    tr.appendChild(document.createElement('th'));
    tr.appendChild(document.createElement('th'));

    thead.appendChild(tr);
    return thead;
}

// criar funcao para listar reservas

function criarLinhaReserva(reserva) {
    const tr = document.createElement('tr');

    COLUNAS.forEach(coluna => {
        const td = document.createElement('td');
        const valor = coluna.valor(reserva);
        td.textContent = coluna.formatar ? coluna.formatar(valor) : valor;
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

montarFiltroEstado()
carregarReservas();
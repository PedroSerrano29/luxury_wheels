const token = localStorage.getItem('token');
if (!token) {
    window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
}

async function carregarReservas() {
    const resultado = await buscarReservas();


    if (!resultado.ok) {
            window.location.href = `login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
            return;
        }

    desenharReservas(resultado.dados);
}

// criar funcao para listar reservas

function criarCartaoReserva(reserva) {
    const card = document.createElement('div');
    card.className = 'reserva-card';

    const titulo = document.createElement('h3');
    titulo.textContent = `${reserva.veiculo.marca} ${reserva.veiculo.modelo}`;
    card.appendChild(titulo);

    card.appendChild(criarLinha('Matrícula', reserva.veiculo.matricula));

    card.appendChild(criarLinha('Data início', reserva.data_inicio));

    card.appendChild(criarLinha('Data fim', reserva.data_fim));

    card.appendChild(criarLinha('Valor total', `${reserva.valor_total}€`))

    card.appendChild(criarLinha('Estado', reserva.estado));

    if (reserva.estado === 'Ativa') {
        // Botão de Cancelar reserva
        const botaoCancelar = document.createElement('button');
        botaoCancelar.textContent = 'Cancelar';
        botaoCancelar.className = 'botao-principal';
        card.appendChild(botaoCancelar);

        botaoCancelar.addEventListener('click', async () => {
            const resultado = await cancelarReserva(reserva.id)
            
            if (!resultado.ok) {
                alert(resultado.dados.erro);
            } else {
                carregarReservas();
            }
        });
    }

    return card
}

function desenharReservas(reservas) {
    const container = document.getElementById('lista-reservas');;
    container.innerHTML = '';

    reservas.forEach(reserva => {
        const card = criarCartaoReserva(reserva);
        container.appendChild(card);
    });
}

carregarReservas();
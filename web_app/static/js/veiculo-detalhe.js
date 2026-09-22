function obterIdDoURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}


function montarPainelReserva(veiculo) {
    const painel = document.getElementById('painel-reserva');
    painel.innerHTML = '';

    // Veículo indisponível (inspeção, revisão, manutenção): a API diz o motivo
    if (veiculo.motivo_indisponibilidade) {
        const titulo = document.createElement('h2');
        titulo.textContent = 'Indisponível';

        const mensagem = document.createElement('p');
        mensagem.className = 'mensagem-indisponivel';
        mensagem.textContent = `Este veículo não está disponível para aluguer: ${veiculo.motivo_indisponibilidade}`;

        painel.appendChild(titulo);
        painel.appendChild(mensagem);
        return;
    }

    const token = localStorage.getItem('token');

    if (!token) {
        const titulo = document.createElement('h2');
        titulo.textContent = 'Reservar';

        const mensagem = document.createElement('p');
        mensagem.textContent = 'Iniciar sessão para efetuar uma reserva.';

        const link = document.createElement('a');
        link.href = `login.html?redirect=${encodeURIComponent(window.location.pathname + window.location.search)}`;
        link.className = 'botao-principal';
        link.textContent = 'Iniciar sessão';

        painel.appendChild(titulo);
        painel.appendChild(mensagem);
        painel.appendChild(link);
        return;
    }
    const titulo = document.createElement('h2');
    titulo.textContent = 'Reservar';
    painel.appendChild(titulo);

    // formulário

    const campoDataInicio = document.createElement('div');
    campoDataInicio.className = 'campo-filtro';

    const labelInicio = document.createElement('label');
    labelInicio.setAttribute('for', 'reserva-data-inicio');
    labelInicio.textContent = 'Data início:';

    const inputInicio = document.createElement('input');
    inputInicio.type = 'date';
    inputInicio.id = 'reserva-data-inicio';

    campoDataInicio.appendChild(labelInicio);
    campoDataInicio.appendChild(inputInicio);
    painel.appendChild(campoDataInicio);

    const campoDataFim = document.createElement('div');
    campoDataFim.className = 'campo-filtro';

    const labelFim = document.createElement('label');
    labelFim.setAttribute('for', 'reserva-data-fim');
    labelFim.textContent = 'Data fim:';

    const inputFim = document.createElement('input');
    inputFim.type = 'date';
    inputFim.id = 'reserva-data-fim';

    campoDataFim.appendChild(labelFim);
    campoDataFim.appendChild(inputFim);
    painel.appendChild(campoDataFim);

    // Apresenta Opçoes de Pagamento
    const opcoesPagamento = [
        {valor: 'Cartão', texto: 'Cartão'},
        {valor: 'MB Way', texto: 'MB Way'}
    ];
    const campoPagamento = criarCampoSelect('reserva-forma-pagamento', 'Forma de pagamento:', opcoesPagamento);
    painel.appendChild(campoPagamento);

    // Apresenta total da Reserva
    const totalReserva = document.createElement('p');
    totalReserva.id = 'reserva-total';
    painel.appendChild(totalReserva);

    // O cálculo é feito pela API; aqui só se mostra o resultado
    async function atualizarTotal() {
        if (!inputInicio.value || !inputFim.value) {
            totalReserva.textContent = '';
            return;
        }

        try {
            const resultado = await calcularOrcamento(veiculo.id, inputInicio.value, inputFim.value);

            if (!resultado.ok) {
                totalReserva.textContent = resultado.dados.erro;
            } else {
                const orcamento = resultado.dados;
                totalReserva.textContent = `Total: ${orcamento.valor_total}€ (${orcamento.numero_dias} dias × ${orcamento.valor_diaria}€)`;
            }
        } catch (erro) {
            console.error('Erro ao calcular o total:', erro);
            totalReserva.textContent = 'Não foi possível calcular o total.';
        }
    }
    inputInicio.addEventListener('change', atualizarTotal);
    inputFim.addEventListener('change', atualizarTotal);

    // Botão de confirmar reserva
    const botaoConfirmar = document.createElement('button');
    botaoConfirmar.textContent = 'Confirmar reserva';
    botaoConfirmar.className = 'botao-principal';
    painel.appendChild(botaoConfirmar);

    const mensagemReserva = document.createElement('p');
    mensagemReserva.id = 'reserva-mensagem';
    painel.appendChild(mensagemReserva);

    botaoConfirmar.addEventListener('click', async () => {
        const dataInicio = inputInicio.value;
        const dataFim = inputFim.value;
        const formaPagamento = document.getElementById('reserva-forma-pagamento').value;
        const resultado = await criarReserva(veiculo.id, dataInicio, dataFim, formaPagamento);
        
        if (!resultado.ok) {
            mensagemReserva.textContent = resultado.dados.erro;
        } else {
            mensagemReserva.textContent = `Reserva criada com sucesso! Valor total: ${resultado.dados.valor_total}€. `;

            const linkReservas = document.createElement('a');
            linkReservas.href = 'minhas-reservas.html';
            linkReservas.textContent = 'Ver as minhas reservas';
            mensagemReserva.appendChild(linkReservas);
        }
    });
}

async function carregarDetalheVeiculo() {
    const id = obterIdDoURL();
    const resultado = await buscarVeiculo(id);
    
    const container = document.getElementById('info-veiculo');
    container.innerHTML = '';

    // Veiculo que não existe (404)
    if (!resultado.ok) {
        const mensagem = document.createElement('p');
        mensagem.textContent = resultado.dados.erro;
        container.appendChild(mensagem);
        return;
    }

    const veiculo = resultado.dados;

    const titulo = document.createElement('h1');
    titulo.textContent = `${veiculo.marca} ${veiculo.modelo}`;

    const imagem = document.createElement('img');
    imagem.src = 'static/images/' + veiculo.imagem_url;
    imagem.className = 'detalhe-imagem';

    container.appendChild(titulo);
    container.appendChild(imagem);
    container.appendChild(criarLinha('Categoria', veiculo.categoria));
    container.appendChild(criarLinha('Transmissão', veiculo.transmissao));
    container.appendChild(criarLinha('Capacidade', `${veiculo.capacidade_pessoas} pessoas`));
    container.appendChild(criarLinha('Combustível', veiculo.combustivel));
    container.appendChild(criarLinha('Valor', `${veiculo.valor_diaria}€ / dia`));

    montarPainelReserva(veiculo);
}

carregarDetalheVeiculo().catch(erro => {
    console.error('Erro ao carregar o veículo:', erro);
    mostrarErroLigacao('info-veiculo');
});
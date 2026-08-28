function obterIdDoURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function criarLinha(rotulo, valor) {
    const p = document.createElement('p');

    const spanRotulo = document.createElement('span');
    spanRotulo.className = 'rotulo-detalhe';
    spanRotulo.textContent = `${rotulo}: `;

    const spanValor = document.createElement('span');
    spanValor.textContent = valor;

    p.appendChild(spanRotulo);
    p.appendChild(spanValor);
    
    return p;
}

function montarPainelReserva(veiculo) {
    const painel = document.getElementById('painel-reserva');
    painel.innerHTML = '';

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

    // Apresentar Opçoes de Pagamento
    const opcoesPagamento = [
        {valor: 'Cartão', texto: 'Cartão'},
        {valor: 'MB Way', texto: 'MB Way'}
    ];
    const campoPagamento = criarCampoSelect('reserva-forma-pagamento', 'Forma de pagamento:', opcoesPagamento);
    painel.appendChild(campoPagamento);
}

async function carregarDetalheVeiculo() {
    const id =obterIdDoURL();
    const veiculo = await buscarVeiculo(id);
    
    const container = document.getElementById('info-veiculo');
    container.innerHTML = '';

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

carregarDetalheVeiculo()
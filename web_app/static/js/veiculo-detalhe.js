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
        link.href = 'login.html';
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
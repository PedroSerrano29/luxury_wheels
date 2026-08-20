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

async function carregarDetalheVeiculo() {
    const id =obterIdDoURL();
    const veiculo = await buscarVeiculo(id);
    
    const container = document.getElementById('detalhe-veiculo');
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
}

carregarDetalheVeiculo()
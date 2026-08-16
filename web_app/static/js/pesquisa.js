function criarCartaoVeiculo(veiculo) {
    const card = document.createElement('div');
    card.className = 'veiculo-card';

    const titulo = document.createElement('h3');
    titulo.textContent = `${veiculo.marca} ${veiculo.modelo}`;

    const imagem = document.createElement('img');
    imagem.src = 'static/images/' + veiculo.imagem_url;

    const info = document.createElement('p');
    info.textContent = `${veiculo.categoria} — ${veiculo.transmissao}`;

    const preco = document.createElement('p');
    preco.textContent = `${veiculo.valor_diaria}€ / dia`;

    card.appendChild(titulo);
    card.appendChild(imagem);
    card.appendChild(info);
    card.appendChild(preco);

    return card;
}

function desenharVeiculos(veiculos) {
    const container = document.getElementById('lista-veiculos');;
    container.innerHTML = '';

    veiculos.forEach(veiculo => {
        const card = criarCartaoVeiculo(veiculo);
        container.appendChild(card);
    });
}


async function carregarVeiculos() {
    const veiculos = await buscarVeiculos();
    desenharVeiculos(veiculos);
}
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

function criarCampoSelect(id, label, opcoes) {
    const container = document.createElement('div');
    container.className = 'campo-filtro';

    const rotulo = document.createElement('label');
    rotulo.setAttribute('for', id);
    rotulo.textContent = label;

    const select = document.createElement('select');
    select.id = id;

    opcoes.forEach(opcao => {
        const option = document.createElement('option');
        option.value = opcao.valor;
        option.textContent = opcao.texto;
        select.appendChild(option);
    });

    container.appendChild(rotulo);
    container.appendChild(select);

    return container;
}

// Mensagem quando a API não responde, dentro do container indicado
function mostrarErroLigacao(idContainer) {
    const container = document.getElementById(idContainer);
    container.innerHTML = '';

    const mensagem = document.createElement('p');
    mensagem.textContent = 'Não foi possível ligar ao servidor. Por favor, tente novamente.';

    const botaoTentar = document.createElement('button');
    botaoTentar.textContent = 'Tentar novamente';
    botaoTentar.className = 'botao-principal';
    botaoTentar.addEventListener('click', () => location.reload());

    container.appendChild(mensagem);
    container.appendChild(botaoTentar);
}
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

function criarPainelFiltros() {
    const painel = document.createElement('div');
    painel.className = 'filtros';

    const titulo = document.createElement('h2');
    titulo.textContent = 'Filtrar';
    painel.appendChild(titulo);

    const campoTipo = criarCampoSelect('filtro-tipo', 'Tipo:', [
        { valor: '', texto: '— Todos —' },
        { valor: 'Carro', texto: 'Carro' },
        { valor: 'Moto', texto: 'Moto' }
    ]);
    painel.appendChild(campoTipo);

    const campoCategoria = criarCampoSelect('filtro-categoria', 'Categoria:', [
        { valor: '', texto: '— Todas —' }
    ]);
    painel.appendChild(campoCategoria);

    const campoValorMaximo = criarCampoNumero('filtro-valor-maximo', 'Valor máximo/dia (€): ', 'Ex: 80');
    painel.appendChild(campoValorMaximo);

    const campoTransmissao = criarCampoSelect('filtro-transmissao', 'Transmissão:', [
        { valor: '', texto: '— Todas —' },
        { valor: 'Automática', texto: 'Automática' },
        { valor: 'Manual', texto: 'Manual' }
    ]);
    painel.appendChild(campoTransmissao);

    const campoCapacidade = criarCampoSelect('filtro-capacidade', 'Nº de pessoas:', [
        { valor: '', texto: '— Todas —' },
        { valor: '1-4', texto: '1 a 4' },
        { valor: '5-6', texto: '5 a 6' },
        { valor: 'mais_de_7', texto: 'Mais de 7' }
    ]);
    painel.appendChild(campoCapacidade);

    return painel
}

function ativarFiltragemAutomatica() {
    const campos = ['filtro-tipo', 'filtro-categoria', 'filtro-transmissao', 'filtro-valor-maximo', 'filtro-capacidade'];

    campos.forEach(id => {
        document.getElementById(id).addEventListener('change', aplicarFiltro);
    });

    document.getElementById('filtro-tipo').addEventListener('change', () => {
        atualizarOpcoesCategoria();
        aplicarFiltro();
    });
}

function criarCampoNumero(id, label, placeholder) {
    const container = document.createElement('div');
    container.className = 'campo-filtro';

    const rotulo = document.createElement('label');
    rotulo.setAttribute('for', id);
    rotulo.textContent = label;

    const input = document.createElement('input');
    input.type = 'number';
    input.id = id;
    input.min = '0';
    input.placeholder = placeholder;

    container.appendChild(rotulo);
    container.appendChild(input);

    return container;
}

async function aplicarFiltro() {
    const tipo = document.getElementById('filtro-tipo').value;
    const categoria = document.getElementById('filtro-categoria').value;
    const transmissao = document.getElementById('filtro-transmissao').value;
    const valorMaximo = document.getElementById('filtro-valor-maximo').value;
    const capacidade = document.getElementById('filtro-capacidade').value;

    const params = new URLSearchParams();

    if (tipo) params.append('tipo', tipo);
    if (categoria) params.append('categoria', categoria);
    if (transmissao) params.append('transmissao', transmissao);
    if (valorMaximo) params.append('valor_maximo', valorMaximo);
    if (capacidade) params.append('capacidade', capacidade);

    const resposta = await fetch(`http://127.0.0.1:5000/api/veiculos?${params.toString()}`);
    const veiculos = await resposta.json();

    desenharVeiculos(veiculos);
}

const OPCOES_CATEGORIA = {
    'Carro': ['Pequeno', 'Médio', 'Grande', 'SUV', 'Luxo'],
    'Moto': ['Naked', 'Scooter', 'Touring', 'Moto']
};

function atualizarOpcoesCategoria() {
    const tipoSelecionado = document.getElementById('filtro-tipo').value;
    const selectCategoria = document.getElementById('filtro-categoria');

    selectCategoria.innerHTML ='';

    const opcaoTodas = document.createElement('option');
    opcaoTodas.value = '';
    opcaoTodas.textContent = '— Todas —';
    selectCategoria.appendChild(opcaoTodas);

    let categorias;
    if (tipoSelecionado === '') {
        categorias = [...OPCOES_CATEGORIA['Carro'], ...OPCOES_CATEGORIA['Moto']];
    } else {
        categorias = OPCOES_CATEGORIA[tipoSelecionado] || [];
    }

    categorias.forEach(cat => {
        const opcao = document.createElement('option');
        opcao.value = cat;
        opcao.textContent = cat;
        selectCategoria.appendChild(opcao);
    });
}
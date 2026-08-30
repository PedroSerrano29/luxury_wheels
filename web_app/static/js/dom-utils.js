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
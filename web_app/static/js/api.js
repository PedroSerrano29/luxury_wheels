async function buscarVeiculos() {
    try {
        const resposta = await fetch('http://127.0.0.1:5000/api/veiculos');
        const dados = await resposta.json();
        return dados;
    } catch (erro) {
        console.error('Erro:', erro);
    }
}
async function buscarVeiculos() {
    try {
        const resposta = await fetch('http://127.0.0.1:5000/api/veiculos');
        const dados = await resposta.json();
        return dados;
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

async function loginClient(email, password) {
    const resposta = await fetch('http://127.0.0.1:5000/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: email, password: password })
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}
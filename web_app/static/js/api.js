async function buscarVeiculos() {
    try {
        const resposta = await fetch('http://127.0.0.1:5000/api/veiculos');
        const dados = await resposta.json();
        return dados;
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

async function loginCliente(email, password) {
    const resposta = await fetch('http://127.0.0.1:5000/api/auth/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({ email: email, password: password })
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}

async function registarCliente(nome, email, password, passwordConfirm) {
    const resposta = await fetch('http://127.0.0.1:5000/api/auth/registo', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({nome:nome, email: email, password: password, password_confim: passwordConfirm })
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}
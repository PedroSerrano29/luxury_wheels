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
        body: JSON.stringify({nome:nome, email: email, password: password, password_confirm: passwordConfirm })
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}

async function buscarVeiculo(id) {
    try {
        const resposta = await fetch(`http://127.0.0.1:5000/api/veiculos/${id}`);
        const dados = await resposta.json();
        return dados;
    } catch (erro) {
        console.error('Erro:', erro);
    }
}

async function criarReserva(veiculoId, dataInicio, dataFim, formaPagamentoTipo) {
    const resposta =await fetch('http://127.0.0.1:5000/api/reservas', {
        method: 'POST',
        headers: {'Content-Type': 'application/json', 'Authorization': localStorage.getItem('token')},
        body: JSON.stringify({veiculo_id:veiculoId, data_inicio:dataInicio, data_fim:dataFim, forma_pagamento_tipo:formaPagamentoTipo})
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}

async function buscarReservas() {
    const resposta =await fetch('http://127.0.0.1:5000/api/reservas', {
        method: 'GET',
        headers: {'Content-Type': 'application/json', 'Authorization': localStorage.getItem('token')},
    });

    const dados = await resposta.json();

    return { ok: resposta.ok, dados: dados};
}
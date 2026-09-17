// true se o token já expirou ou não se consegue ler
function tokenExpirado(token) {
    try {
        const payloadBase64 = token.split('.')[1].replaceAll('-', '+').replaceAll('_', '/');
        const payload = JSON.parse(atob(payloadBase64));

        if (typeof payload.exp !== 'number') {
            return true;
        }

        return payload.exp * 1000 <= Date.now();
    } catch (erro) {
        return true;
    }
}

function atualizarNavbar() {
    const token = localStorage.getItem('token');
    const nome = localStorage.getItem('nome');
    const botoesContainer = document.querySelector('.navbar-botoes');

    if(!botoesContainer) return;

    botoesContainer.innerHTML = '';

    if (token) {
        const saudacao = document.createElement('span');
        saudacao.className = 'navbar-saudacao';
        saudacao.textContent = `Olá, ${nome}`;

        const botaoMinhasReservas = document.createElement('a');
        botaoMinhasReservas.href = 'minhas-reservas.html';
        botaoMinhasReservas.textContent = 'Minhas Reservas';

        const botaoSair = document.createElement('button');
        botaoSair.textContent = 'Sair';
        botaoSair.addEventListener('click', fazerLogout);

        botoesContainer.appendChild(saudacao);
        botoesContainer.appendChild(botaoMinhasReservas)
        botoesContainer.appendChild(botaoSair);
    } else {
        const botaoLogin = document.createElement('a');
        botaoLogin.href = 'login.html';
        botaoLogin.textContent = 'Login';

        const botaoRegisto = document.createElement('a');
        botaoRegisto.href = 'registo.html';
        botaoRegisto.textContent = 'Registar-se';

        botoesContainer.appendChild(botaoLogin);
        botoesContainer.appendChild(botaoRegisto);
    }
}

// Apaga token e nome guardados
function limparSessao() {
    localStorage.removeItem('token');
    localStorage.removeItem('nome');
}

function fazerLogout() {
    limparSessao();
    window.location.href= 'index.html';
}

// Limpar a sessão se o token guardado já expirou
function verificarSessaoExpirada() {
    const token = localStorage.getItem('token');

    if(token && tokenExpirado(token)) {
        limparSessao();
        sessionStorage.setItem('sessaoExpirada', 'sim');
    }
}

verificarSessaoExpirada();
atualizarNavbar();
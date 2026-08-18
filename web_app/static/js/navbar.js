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

        const botaoSair = document.createElement('button');
        botaoSair.textContent = 'Sair';
        botaoSair.addEventListener('click', fazerLogout);

        botoesContainer.appendChild(saudacao);
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

function fazerLogout() {
    localStorage.removeItem('token');
    localStorage.removeItem('nome');
    window.location.href = 'index.html';
}

atualizarNavbar();
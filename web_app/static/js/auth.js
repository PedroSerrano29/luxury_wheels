const formLogin = document.getElementById('form-login');
if (formLogin) {
    formLogin.addEventListener('submit', async (evento) => {
        evento.preventDefault();

        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const caixaErro = document.getElementById('login-erro');

        const resultado = await loginCliente(email, password);

        if(!resultado.ok) {
            caixaErro.textContent = resultado.dados.erro;
            return;
        }

        localStorage.setItem('token', resultado.dados.token);
        localStorage.setItem('nome', resultado.dados.nome);

        const params = new URLSearchParams(window.location.search);
        const redirect = params.get('redirect');
        window.location.href = redirect || 'index.html';
    });
}

const formRegisto = document.getElementById('form-registo');
if (formRegisto) {
    formRegisto.addEventListener('submit', async (evento) => {
        evento.preventDefault();

        const nome = document.getElementById('registo-nome').value;
        const email = document.getElementById('registo-email').value;
        const password = document.getElementById('registo-password').value;
        const passwordConfirm = document.getElementById('registo-password-confirm').value;
        const caixaErro = document.getElementById('registo-erro');

        const resultado = await registarCliente(nome, email, password, passwordConfirm);

        if (!resultado.ok) {
            caixaErro.textContent = resultado.dados.erro;
            return;
        }

        window.location.href = 'login.html';
    });
}


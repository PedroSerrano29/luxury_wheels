document.getElementById('form-login').addEventListener('submit', async (evento) => {
    evento.preventDefault();

    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    const caixaErro = document.getElementById('login-erro');

    const resultado = await loginClient(email, password);

    if(!resultado.ok) {
        caixaErro.textContent = resultado.dados.erro;
        return;
    }

    localStorage.setItem('token', resultado.dados.token);
    localStorage.setItem('nome', resultado.dados.nome);
    window.location.href = 'index.html';
});
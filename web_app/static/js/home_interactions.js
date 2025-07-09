document.addEventListener("DOMContentLoaded", function () {
    // Exemplo: Destacar o botão do utilizador autenticado
    const userCircle = document.querySelector('.user-circle');
    if (userCircle) {
        userCircle.title = "Ir para o perfil";
        userCircle.style.border = "2px solid #fff";
        userCircle.style.boxShadow = "0 0 0 3px #007bff44";
    }

    // Exemplo: Mostrar mensagem ao clicar em "Reservar" se o veículo estiver indisponível
    document.querySelectorAll('.indisponivel-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            alert("Este veículo está indisponível.");
        });
    });
});
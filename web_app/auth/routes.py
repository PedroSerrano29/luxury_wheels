from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user
from werkzeug.security import check_password_hash
from database.setup_database import Cliente, session
from flask_mail import Message
from web_app.auth.utils import send_email  # Função de envio de email

import random
import string
from werkzeug.security import generate_password_hash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        cliente = session.query(Cliente).filter_by(email=email).first()
        if cliente and check_password_hash(cliente.senha, senha):
            login_user(cliente)
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Email ou senha incorretos.', 'danger')

    return render_template('login.html')



@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        primeiro_nome = request.form['primeiro_nome']
        ultimo_nome = request.form['ultimo_nome']
        email = request.form['email']
        senha = request.form['senha']
        confirmar = request.form['confirmar']

        if senha != confirmar:
            flash("As passwords não coincidem.", "danger")
            return render_template("register.html")

        if session.query(Cliente).filter_by(email=email).first():
            flash("Já existe uma conta com este email.", "warning")
            return render_template("register.html")

        nome_completo = f"{primeiro_nome} {ultimo_nome}"
        hash_senha = generate_password_hash(senha)

        novo_cliente = Cliente(nome=nome_completo, email=email, senha=hash_senha)
        session.add(novo_cliente)
        session.commit()

        # Envia email de confirmação
        send_email(
            subject="Registo na Luxury Wheels",
            recipients=[email],
            body=f"Olá {nome_completo}, o seu registo foi concluído com sucesso!"
        )

        flash("Registo efetuado com sucesso! Pode agora fazer login.", "success")
        return redirect(url_for('auth.login'))

    return render_template('register.html')

@auth_bp.route('/recuperar-password', methods=['GET', 'POST'])
def recuperar_password():
    if request.method == 'POST':
        email = request.form['email']
        cliente = session.query(Cliente).filter_by(email=email).first()

        if not cliente:
            flash("Email não encontrado na base de dados.", "danger")
            return render_template("recuperar.html")

        # Gerar nova password aleatória
        nova_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        cliente.senha = generate_password_hash(nova_password)
        session.commit()

        # Enviar nova password por email
        send_email(
            subject="Recuperação de Password - Luxury Wheels",
            recipients=[email],
            body=f"Olá {cliente.nome},\n\nA sua nova password é: {nova_password}\n\nRecomendamos que a altere após o login."
        )

        flash("Foi enviada uma nova password para o seu email.", "success")
        return redirect(url_for('auth.login'))

    return render_template('recuperar_password.html')
from flask import Flask, request, render_template
from datetime import datetime, timedelta
from sqlalchemy import or_, and_
from flask_login import LoginManager
from database.setup_database import Cliente
from web_app.auth.routes import auth_bp
from web_app.auth.utils import mail

# Adiciona o path do projeto
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Importa os modelos e sessão
from database.setup_database import Veiculo, Reserva, session

# Cria a app Flask
app = Flask(__name__)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Regista o blueprint de autenticação
app.register_blueprint(auth_bp)

# Define como carregar o utilizador
@login_manager.user_loader
def load_user(user_id):
    return session.query(Cliente).get(int(user_id))

@app.route('/')
def home():
    query = session.query(Veiculo)

    # Filtros via GET
    categoria = request.args.get('categoria')
    combustivel = request.args.get('combustivel')
    transmissao = request.args.get('transmissao')

    tipo = request.args.get('tipo')
    lugares = request.args.get('lugares')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if categoria:
        query = query.filter_by(categoria=categoria)
    if combustivel:
        query = query.filter_by(combustivel=combustivel)
    if transmissao:
        query = query.filter_by(transmissao=transmissao)
    if tipo:
        query = query.filter_by(tipo=tipo)
    if lugares:
        if lugares == '1-4':
            query = query.filter(Veiculo.lugares.between(1, 4))
        elif lugares == '5-6':
            query = query.filter(Veiculo.lugares.between(5, 6))
        elif lugares == '7+':
            query = query.filter(Veiculo.lugares >= 7)

    hoje = datetime.today().date()
    um_ano_atras = hoje - timedelta(days=365)

    veiculos = query.all()
    veiculos_info = []

    for veiculo in veiculos:
        indisponivel = False
        motivos = []

        # Verificações de disponibilidade
        if not veiculo.disponivel:
            indisponivel = True
            # motivos.append('Disponibilidade desativada')

        if veiculo.ultima_inspecao and veiculo.ultima_inspecao < um_ano_atras:
            indisponivel = True
            # motivos.append('Inspeção fora de validade')

        if veiculo.proxima_revisao and veiculo.proxima_revisao <= hoje:
            indisponivel = True
            # motivos.append('Revisão expirada')

        # Verifica conflitos com reservas
        if data_inicio and data_fim:
            try:
                inicio = datetime.strptime(data_inicio, "%Y-%m-%d").date()
                fim = datetime.strptime(data_fim, "%Y-%m-%d").date()

                reservas_existentes = session.query(Reserva).filter(
                    Reserva.veiculo_id == veiculo.id,
                    Reserva.data_inicio <= fim,
                    Reserva.data_fim >= inicio
                ).all()

                if reservas_existentes:
                    indisponivel = True
                    # motivos.append('Reservado no período selecionado')
            except ValueError:
                pass  # Ignora datas mal formatadas

        veiculos_info.append({
            'id': veiculo.id,
            'marca': veiculo.marca,
            'modelo': veiculo.modelo,
            'categoria': veiculo.categoria,
            'transmissao': veiculo.transmissao,
            'tipo': veiculo.tipo,
            'lugares': veiculo.lugares,
            'valor_diaria': veiculo.diaria,
            'imagem': veiculo.imagem if veiculo.imagem else 'default.jpg',
            'indisponivel': indisponivel,
            'motivos': motivos
        })

    return render_template('home.html', veiculos=veiculos_info)

# Configurações do email
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'luxurywheelspedroserrano@gmail.com'
app.config['MAIL_PASSWORD'] = 'luxurywheelspedroserrano29'
app.config['MAIL_DEFAULT_SENDER'] = 'luxurywheelspedroserrano@gmail.com'

mail.init_app(app)

# Inicia o servidor Flask
if __name__ == '__main__':
    app.run(debug=True)

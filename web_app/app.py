import sys

from flask import Flask, request, render_template, flash
from datetime import datetime, timedelta
from flask_login import LoginManager
from dotenv import load_dotenv
import os
import logging
from flask_mail import Mail

from web_app.extensions import mail  # Import mail from extensions
from web_app.auth.routes import auth_bp
from web_app.utils import apply_filter
from database.setup_database import Veiculo, Reserva, session, Cliente

# Load environment variables
load_dotenv()
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Create Flask app
app = Flask(__name__)

# Configure app
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS', 'True').lower() == 'true'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

# Initialize mail
mail = Mail(app)

# Initialize extensions
mail.init_app(app)

# Login Manager
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')

# Define user loader
@login_manager.user_loader
def load_user(user_id):
    return session.query(Cliente).get(int(user_id))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    try:
        query = session.query(Veiculo)

        # Filtros via GET
        categoria = request.args.get('categoria')
        combustivel = request.args.get('combustivel')
        transmissao = request.args.get('transmissao')
        tipo = request.args.get('tipo')
        lugares = request.args.get('lugares')
        data_inicio = request.args.get('data_inicio')
        data_fim = request.args.get('data_fim')

        # Aplica os filtros
        query = apply_filter(query, 'categoria', categoria)
        query = apply_filter(query, 'combustivel', combustivel)
        query = apply_filter(query, 'transmissao', transmissao)
        query = apply_filter(query, 'tipo', tipo)

        if lugares:
            if lugares == '1-4':
                query = query.filter(Veiculo.lugares.between(1, 4))
            elif lugares == '5-6':
                query = query.filter(Veiculo.lugares.between(5, 6))
            elif lugares == '7+':
                query = query.filter(Veiculo.lugares >= 7)

        # Paginação manual
        page = request.args.get('page', 1, type=int)
        per_page = 9
        total_veiculos = query.count()  # Número total de veículos
        paginated_veiculos = query.offset((page - 1) * per_page).limit(per_page).all()

        veiculos_info = []
        hoje = datetime.today().date()
        um_ano_atras = hoje - timedelta(days=365)

        for veiculo in paginated_veiculos:
            indisponivel = False
            motivos = []

            # Verifica disponibilidade
            if not veiculo.disponivel:
                indisponivel = True
                motivos.append('Disponibilidade desativada')

            if veiculo.ultima_inspecao and veiculo.ultima_inspecao < um_ano_atras:
                indisponivel = True
                motivos.append('Inspeção fora de validade')

            if veiculo.proxima_revisao and veiculo.proxima_revisao <= hoje:
                indisponivel = True
                motivos.append('Revisão expirada')

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
                        motivos.append('Reservado no período selecionado')
                except ValueError:
                    flash("Formato de data inválido. Use o formato AAAA-MM-DD.", "error")

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

        logger.info("Home route accessed successfully.")
        return render_template('home.html', veiculos=veiculos_info, total=total_veiculos, page=page, per_page=per_page)
    except Exception as e:
        logger.error(f"Error in home route: {e}")
        flash("Ocorreu um erro ao carregar os veículos.", "error")
        return render_template('home.html', veiculos=[])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)

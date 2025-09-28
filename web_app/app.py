import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import request, render_template, Flask, redirect, url_for, flash
from datetime import datetime, timedelta
from database.setup_database import Veiculo, Reserva, session
from sqlalchemy import or_, and_
from flask_dance.contrib.google import make_google_blueprint, google
import os
from flask import session as flask_session

app = Flask(__name__)

app.secret_key = os.environ.get("FLASK_SECRET_KEY", "supersecret")
google_bp = make_google_blueprint(
    client_id=os.environ.get("GOOGLE_OAUTH_CLIENT_ID"),
    client_secret=os.environ.get("GOOGLE_OAUTH_CLIENT_SECRET"),
    redirect_to="index"
)
app.register_blueprint(google_bp, url_prefix="/login")

def home_data():
    query = session.query(Veiculo)

    # Filtros via GET
    categoria = request.args.get('categoria')
    transmissao = request.args.get('transmissao')
    tipo = request.args.get('tipo')
    lugares = request.args.get('lugares')
    data_inicio = request.args.get('data_inicio')
    data_fim = request.args.get('data_fim')

    if categoria:
        query = query.filter_by(categoria=categoria)
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
            motivos.append('Disponibilidade desativada')

        if veiculo.ultima_inspecao and veiculo.ultima_inspecao < um_ano_atras:
            indisponivel = True
            motivos.append('Inspeção fora de validade')

        if veiculo.proxima_revisao and veiculo.proxima_revisao <= hoje:
            indisponivel = True
            motivos.append('Revisão expirada')

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
                    motivos.append('Reservado no período selecionado')
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

    return veiculos_info

@app.route("/", methods=["GET"])
def index():
    # Dynamic filter options
    brands = [b[0] for b in session.query(Veiculo.marca).distinct().all()]
    categories = [c[0] for c in session.query(Veiculo.categoria).distinct().all()]
    transmissoes = [t[0] for t in session.query(Veiculo.transmissao).distinct().all()]
    tipos = [tp[0] for tp in session.query(Veiculo.tipo).distinct().all()]
    lugares_opts = sorted(set([v.lugares for v in session.query(Veiculo).all()]))

    # Use home() logic for filtered vehicles
    veiculos_info = home_data()  # Move your home() logic to a helper function

    user = flask_session.get("user")  # Get user info from session

    return render_template(
        "home.html",
        brands=brands,
        categories=categories,
        transmissoes=transmissoes,
        tipos=tipos,
        lugares_opts=lugares_opts,
        veiculos=veiculos_info,
        user=user
    )

@app.route("/login/google")
def login_google():
    if not google.authorized:
        return redirect(url_for("google.login"))
    resp = google.get("/oauth2/v2/userinfo")
    assert resp.ok, resp.text
    user_info = resp.json()
    flask_session["user"] = user_info  # Store user info in session
    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    flask_session.pop("user", None)
    flash("Logged out.")
    return redirect(url_for("index"))

@app.route("/veiculo/<int:veiculo_id>", methods=["GET", "POST"])
def veiculo_detail(veiculo_id):
    veiculo = session.query(Veiculo).get(veiculo_id)
    if request.method == "POST":
        # Check if user is logged in (via Google)
        if not google.authorized:
            flash("You must be logged in to reserve.")
            return redirect(url_for("login_google"))
        user_info = google.get("/oauth2/v2/userinfo").json()
        # Get reservation dates from form
        data_inicio = request.form["data_inicio"]
        data_fim = request.form["data_fim"]
        # Create reservation
        reserva = Reserva(
            veiculo_id=veiculo_id,
            cliente_email=user_info["email"],
            data_inicio=data_inicio,
            data_fim=data_fim
        )
        session.add(reserva)
        session.commit()
        flash("Reservation successful!")
        return redirect(url_for("index"))
    return render_template("veiculo_detail.html", veiculo=veiculo)

if __name__ == "__main__":
    app.run(debug=True)

# Luxury Wheels

Plataforma de aluguer de veículos (carros e motos) desenvolvida como projeto final do curso de Python da Tokio School — **Proposta A: website para clientes**.

O projeto é composto por uma **API REST em Flask**, que concentra toda a lógica de negócio (validações, cálculos e regras de disponibilidade), e por um **website em HTML, CSS e JavaScript**, que apenas consome a API e mostra os resultados.

## Funcionalidades

- Registo e autenticação de clientes (password guardada com hash, sessão com token JWT)
- Pesquisa de veículos por **marca ou modelo** (ex: `bmw`, `series`, `bmw series 3`)
- Filtros por tipo (Carro/Moto), categoria, transmissão, valor máximo da diária e número de pessoas (1-4, 5-6, mais de 7)
- Página de detalhe do veículo com formulário de reserva: datas de início e fim e forma de pagamento (Cartão ou MB Way)
- **Valor total calculado pela API** (valor da diária × número de dias) antes de confirmar a reserva
- Área "As Minhas Reservas": tabela com filtro por estado, ordenação por coluna, alteração de datas e cancelamento

## Regras de negócio (backend)

- Um veículo fica **indisponível** se a última inspeção obrigatória tiver mais de 1 ano, se a data da próxima revisão já tiver passado, se estiver em manutenção ou se estiver inativo. Os veículos indisponíveis não aparecem na pesquisa, e a página de detalhe mostra o motivo.
- Depois de reservado, o veículo deixa de estar disponível para essas datas: uma reserva que se sobreponha a outra é recusada.
- A data de início não pode ser anterior a hoje, e a data de fim tem de ser posterior à de início.
- O estado da reserva é calculado a partir das datas: **Reservada** (ainda não começou), **Ativa** (a decorrer), **Concluída** ou **Cancelada**.
- Uma reserva *Reservada* pode ser cancelada ou ter as datas de início e fim alteradas. Numa reserva *Ativa* só se pode alterar a data de fim. O valor total é recalculado em cada alteração.

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Backend | Python 3, Flask, Flask-SQLAlchemy, Flask-CORS, PyJWT, Werkzeug (hash de passwords) |
| Base de dados | SQLite (tabelas: veículos, clientes, reservas, formas de pagamento, utilizadores) |
| Frontend | HTML5, CSS3, JavaScript (sem frameworks) |
| Testes | pytest |

## Estrutura

```
luxury_wheels/
├── backend/
│   ├── app.py                   # cria a aplicação Flask e regista as rotas
│   ├── config.py                # configuração (lê a SECRET_KEY do .env)
│   ├── models.py                # modelos SQLAlchemy
│   ├── auth_utils.py            # decorador que valida o token JWT
│   ├── seed.py                  # cria as tabelas e importa os veículos do CSV
│   ├── registar_manutencao.py   # linha de comandos para registar inspeções e revisões
│   ├── routes/                  # veiculos.py, reservas.py, auth.py
│   └── services/                # regras de negócio: veículos, reservas e pagamentos
├── database/
│   ├── schema.sql               # esquema SQL das tabelas
│   └── veiculos.csv             # dados iniciais da frota (40 veículos)
├── web_app/                     # website (páginas HTML, CSS, JavaScript e imagens)
├── tests/                       # testes pytest
└── docs/                        # relatório do projeto (Word)
```

## Como executar

Requisitos: Python 3.10 ou superior.

**1. Instalar as dependências**

```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

pip install -r backend/requirements.txt
```

**2. Criar o ficheiro `backend/.env`** (a partir de `backend/.env.example`) com uma chave secreta, por exemplo:

```bash
python -c "import secrets; open('backend/.env', 'w').write('SECRET_KEY=' + secrets.token_hex(32) + '\n')"
```

**3. Criar a base de dados e importar os veículos**

```bash
cd backend
python seed.py
```

**4. Arrancar a API** (fica em `http://127.0.0.1:5000`)

```bash
python app.py
```

**5. Abrir o website** — noutro terminal, na raiz do projeto:

```bash
cd web_app
python -m http.server 5500
```

e abrir `http://127.0.0.1:5500` no browser.

Para experimentar: registar um cliente em "Registar-se", iniciar sessão e reservar um veículo. O Fiat Panda e o Opel Corsa estão propositadamente fora de validade (inspeção e revisão, respetivamente), para mostrar a regra de disponibilidade — não aparecem na pesquisa, e em `veiculo.html?id=18` e `veiculo.html?id=22` aparece o motivo.

### Registar inspeções e revisões

```bash
cd backend
python registar_manutencao.py                  # lista os veículos indisponíveis e o motivo
python registar_manutencao.py 18 inspecao      # regista uma inspeção feita hoje no veículo 18
python registar_manutencao.py 22 revisao       # regista uma revisão hoje; a próxima fica para daqui a 1 ano
```

## Testes

Na raiz do projeto:

```bash
python -m pytest
```

Os testes usam uma base de dados temporária (não mexem em `database/luxury_wheels.db`) e cobrem a regra de disponibilidade, o cálculo do valor total, a sobreposição de reservas, as datas inválidas, a alteração e o cancelamento de reservas e a validação do registo.

## API

| Método | Rota | Descrição |
|---|---|---|
| POST | `/api/auth/registo` | Registar cliente |
| POST | `/api/auth/login` | Login de cliente (devolve o token) |
| POST | `/api/auth/login-staff` | Login de gestor/administrador |
| GET | `/api/veiculos` | Veículos disponíveis, com pesquisa e filtros (`pesquisa`, `tipo`, `categoria`, `transmissao`, `valor_maximo`, `capacidade_pessoas`) |
| GET | `/api/veiculos/opcoes-filtro` | Valores possíveis para os filtros |
| GET | `/api/veiculos/<id>` | Detalhe do veículo, com o motivo de indisponibilidade (se houver) |
| POST / PUT | `/api/veiculos`, `/api/veiculos/<id>` | Criar e alterar veículos (gestor/admin) |
| PUT | `/api/veiculos/<id>/desativar` | Desativar veículo (gestor/admin) |
| DELETE | `/api/veiculos/<id>` | Apagar veículo sem reservas (admin) |
| GET | `/api/reservas/orcamento` | Valor total para um veículo e um período |
| POST | `/api/reservas` | Criar reserva (cliente autenticado) |
| GET | `/api/reservas` | Reservas do cliente autenticado |
| PUT | `/api/reservas/<id>` | Alterar datas ou cancelar (`{"cancelar": true}`) |

As rotas protegidas recebem o token no cabeçalho `Authorization`.

## Limitações e trabalho futuro

- Aplicação desktop de gestão da frota (Proposta B), que pode reutilizar a mesma API e os mesmos serviços
- Reserva por modelo, com atribuição automática de um veículo concreto quando há vários iguais
- Pagamento real (atualmente só se regista a forma de pagamento escolhida)
- Endereço da API configurável no frontend e publicação num servidor (deploy)

Luxury Wheels — Roadmap de Construção e Estudo
Projeto Final de Python (Tokio School) — Pedro Serrano
1. Decisão de arquitetura (e como a defender na tese)

Escolha: uma API REST central em Flask com duas aplicações cliente:

                    ┌───────────────────────────┐
                    │   Base de Dados           │
                    │  (SQLite → RDS Postgres)  │
                    └──────────▲────────────────┘
                               │
                    ┌──────────┴─────────────┐
                    │   Flask REST API       │  ← lógica de negócio,
                    │   (backend/)           │    validações, regras
                    └───▲────────────────▲───┘
                        │                │
            ┌───────────┴────┐   ┌───────┴────────────┐
            │  Website       │   │  App Desktop       │
            │  HTML+CSS+JS   │   │  Tkinter           │
            │  (Proposta A)  │   │  (Proposta B)      │
            └────────────────┘   └────────────────────┘

Porque é que isto é a escolha certa a defender:

Single source of truth: a regra "veículo fica indisponível após reserva" ou "indisponível se inspeção > 1 ano" vive num só sítio (a API), não duplicada em dois códigos.
Escalabilidade real: amanhã podias adicionar uma app mobile e ela usaria a mesma API sem tocar em nada.
Separação de responsabilidades: front-end (website e desktop) só apresentam dados e recolhem input; toda a validação de negócio está no backend — boa prática de engenharia que qualquer júri reconhece.
É literalmente o que empresas reais fazem (é por isto que dá para "aplicar comercialmente").

Isto substitui a abordagem original do repositório (Flask a renderizar Jinja2 diretamente + Tkinter a falar diretamente com a BD). Vamos mudar para Flask a servir JSON, e tanto o website (via fetch() em JavaScript) como o Tkinter (via requests) consomem essa API.

2. Stack tecnológico
Camada	Tecnologia	Porquê
Base de dados	SQLite (dev) → PostgreSQL no AWS RDS (produção)	SQLite é grátis e local para desenvolver depressa; Postgres no free tier da AWS para simular produção real
Backend / API	Python + Flask + Flask-SQLAlchemy	É o que já tens no repo, é leve, e o ORM ajuda a escrever menos SQL manual sem esconder o que está a acontecer
Autenticação	Flask sessions ou JWT (a decidir na Fase 2)	JWT é mais "profissional" e serve tanto o website como o Tkinter da mesma forma
Website (Proposta A)	HTML + CSS + JavaScript puro (fetch API)	Como querias aprender JS sem framework — dá para perceberes DOM, fetch, promises, antes de saltares para React/Vue no futuro
Desktop (Proposta B)	Python + Tkinter (+ requests para falar com a API)	Mantém-se em Python, reforça essa skill, e usa a mesma API
Deploy	AWS Free Tier: EC2 (API Flask) + RDS (Postgres) + S3 (imagens dos veículos)	Grátis 12 meses, e é o standard da indústria
Documentação	Pasta /docs no repo + este roadmap	Vais construir a documentação enquanto desenvolves, não no fim
3. Estrutura de pastas (atualizada)
luxury_wheels/
│
├── backend/
│   ├── app.py                  # Cria a app Flask, regista blueprints
│   ├── config.py               # Configurações (dev/prod, chave secreta, DB URI)
│   ├── models.py               # Modelos SQLAlchemy (Veiculo, Cliente, Reserva, FormaPagamento, Utilizador)
│   ├── routes/
│   │   ├── veiculos.py         # /api/veiculos (GET, POST, PUT, DELETE)
│   │   ├── clientes.py
│   │   ├── reservas.py
│   │   ├── auth.py             # registo/login
│   │   └── dashboard.py        # endpoints agregados para o dashboard
│   ├── services/               # regras de negócio (disponibilidade, cálculo de preço)
│   └── requirements.txt
│
├── database/
│   ├── schema.sql               # DDL das tabelas
│   ├── seed.py                  # popula dados de teste
│   └── luxury_wheels.db
│
├── web_app/                     # cliente website (Proposta A)
│   ├── templates/                # HTML estático (servido pela própria Flask ou por ficheiro simples)
│   ├── static/
│   │   ├── css/style.css
│   │   ├── js/
│   │   │   ├── api.js            # funções fetch() reutilizáveis
│   │   │   ├── pesquisa.js
│   │   │   ├── reserva.js
│   │   │   └── auth.js
│   │   └── images/
│
├── desktop_app/                  # cliente gestão de frota (Proposta B)
│   ├── main.py
│   ├── api_client.py             # wrapper à volta de `requests` para falar com o backend
│   ├── components/
│   │   ├── login_window.py
│   │   ├── dashboard_window.py
│   │   ├── veiculos_window.py
│   │   ├── clientes_window.py
│   │   └── reservas_window.py
│
├── docs/
│   ├── ARQUITETURA.md
│   ├── MODELO_DADOS.md
│   ├── API.md                    # documentação de cada endpoint
│   ├── DECISOES.md               # ADRs — "porque escolhi X em vez de Y"
│   └── DEPLOY_AWS.md
│
├── tests/
├── .gitignore
└── README.md
4. Modelo de dados (visão inicial — vamos afinar na Fase 1)

veiculos id, marca, modelo, categoria (Pequeno/Médio/Grande/SUV/Luxo), transmissao (Automático/Manual), tipo (Carro/Moto), capacidade_pessoas, valor_diaria, imagem_url, data_ultima_revisao, data_proxima_revisao, data_ultima_inspecao, disponivel (bool), em_manutencao (bool)

clientes id, nome, email, password_hash, data_registo

utilizadores (staff/gestores da frota — só usado pela app desktop) id, nome, email, password_hash, role

formas_pagamento id, cliente_id, tipo (MB Way/Cartão/...), detalhes

reservas id, cliente_id, veiculo_id, data_inicio, data_fim, valor_total, forma_pagamento_id, estado (Ativa/Cancelada/Concluída), data_criacao

Regras de negócio a implementar no backend (retiradas dos critérios técnicos do enunciado):

Um veículo fica indisponível assim que tem uma reserva ativa.
Um veículo fica indisponível se data_ultima_inspecao > 1 ano ou data_proxima_revisao < hoje.
Alteração de reserva só permite mudar datas ou cancelar — nunca trocar de veículo.
Valor total da reserva = valor_diaria × nº_dias.
Dashboard (app desktop) avisa 15 dias antes de revisão/inspeção expirar (a Proposta A pede 15 dias; a Proposta B do critério técnico pede 5 dias antes de revisão — vamos padronizar em 15 dias para ambas e documentar essa decisão em DECISOES.md, já que o enunciado é ambíguo aqui — isto é exatamente o tipo de escolha que tens "liberdade para decidir" e que deves justificar na defesa).
5. Como vais documentar (para a defesa de tese)

Vais criar, desde já, a pasta docs/ e usar este princípio: cada decisão técnica não óbvia gera uma entrada em DECISOES.md, no formato:

md
## Decisão: Autenticação via JWT em vez de sessões Flask
**Contexto:** tanto o website como a app desktop precisam de autenticar-se na mesma API.
**Alternativas consideradas:** sessões Flask (cookies), JWT.
**Escolha:** JWT, porque a app desktop não é um browser e não gere cookies facilmente;
um token enviado no header Authorization funciona igual para os dois clientes.
**Trade-off aceite:** JWT sem refresh token é mais simples mas expira sem renovação automática — aceitável para o âmbito do projeto.

Isto vai ser ouro na defesa — em vez de "fiz assim porque sim", tens 10-15 destas entradas prontas para citar.

6. Roadmap por fases

Ritmo assumido: ~5 sessões de 30-45 min por semana. Ajusta livremente — o importante é a sequência, não o calendário rígido.

FASE 0 — Fundamentos e Setup (Semana 1)

Objetivo: ambiente pronto, BD desenhada, git organizado.

 Dia 1: Criar ambiente virtual Python, reorganizar o repo para a nova estrutura de pastas, git commit.
 Dia 2: Instalar Flask + Flask-SQLAlchemy. Escrever schema.sql com as 5 tabelas.
 Dia 3: Criar models.py com as classes SQLAlchemy correspondentes.
 Dia 4: Escrever seed.py para popular ~15 veículos, 5 clientes de teste.
 Dia 5: Criar docs/ARQUITETURA.md e docs/MODELO_DADOS.md com o que já construímos (usa os diagramas deste roadmap como ponto de partida).

Skill em foco: SQL (schema design), SQLAlchemy ORM.

FASE 1 — Backend API: Veículos e Autenticação (Semana 2-3)
 Endpoint GET /api/veiculos com filtros (categoria, transmissão, tipo, valor, pessoas).
 Endpoint GET /api/veiculos/<id>.
 Endpoints POST/PUT/DELETE /api/veiculos (para o desktop, protegidos por auth de staff). ✅ Feito — POST/PUT/desativar exigem token + role gestor/admin; DELETE exige role admin.
 POST /api/auth/registo e POST /api/auth/login (clientes) — hash de password com werkzeug.security.
 Testar tudo com curl ou Postman/Thunder Client antes de qualquer frontend.
 Documentar cada endpoint em docs/API.md à medida que o crias.

Skill em foco: Flask routing, REST design, segurança básica (hashing).

FASE 2 — Backend API: Reservas e regras de negócio (Semana 3-4)
 POST /api/reservas — calcula valor total, marca veículo indisponível, valida datas. ✅ Feito, incluindo resolução da forma de pagamento por tipo (get-or-create).
 PUT /api/reservas/<id> — alterar datas ou cancelar (liberta o veículo se cancelado). ✅ Feito, e evoluído: agora só permite cancelar reservas "Reservada" e só permite alterar a data_fim de reservas "Ativa" (nunca a data_inicio), com a nova data_fim nunca podendo ser anterior a hoje.
 GET /api/reservas?cliente_id= — histórico do cliente. ✅ Feito (cliente_id vem sempre do token, não é um parâmetro do pedido).
 ✅ Adicionado (não estava no plano original): estado da reserva (Reservada/Ativa/Concluída/Cancelada) deixou de ser um campo fixo e passou a ser calculado a partir das datas — ver DECISOES.md.
 Job/rotina que marca veículos indisponíveis por revisão/inspeção vencida (pode ser uma função chamada a cada pedido, não precisa de scheduler já).
 Escrever 3-5 testes simples com pytest para as regras de negócio (ótimo ponto para a tese: "testei as regras críticas") — por fazer; até agora testado manualmente com curl.

Skill em foco: lógica de negócio, datas em Python (datetime), testes automatizados.

FASE 3 — Website: estrutura e JavaScript (Semana 4-5)
 HTML das páginas: login/registo, listagem+filtros de veículos, detalhe do veículo, reserva, "as minhas reservas". ✅ Feito — todas as páginas existem e funcionam, incluindo minhas-reservas.html.
 api.js: funções fetch() reutilizáveis (GET/POST com tratamento de erro). ✅ Feito — buscarVeiculos, buscarVeiculo, loginCliente, registarCliente, criarReserva, buscarReservas, cancelarReserva.
 pesquisa.js: filtros dinâmicos sem recarregar a página (event listeners, atualizar DOM). ✅ Feito, em filtros.js.
 auth.js: login guarda token (localStorage não existe nos artifacts do Claude, mas no teu site real podes usá-lo), redireciona. ✅ Feito.
 reserva.js: calcular e mostrar valor total em tempo real conforme o cliente muda as datas. ✅ Feito — acabou por ficar dentro de veiculo-detalhe.js (montarPainelReserva) em vez de um ficheiro reserva.js à parte, já que a lógica está diretamente ligada ao resto do painel de reserva dessa página.
 ✅ Adicionado (não estava no plano original): dom-utils.js — funções de construção de DOM partilhadas entre páginas (criarLinha), extraídas para evitar duplicação entre veiculo-detalhe.js e reservas.js.
 ✅ Adicionado: reservas.js — lista as reservas do cliente (cartões com matrícula, datas, valor, estado), com botão de cancelar e verificação de sessão (redireciona para login se o token não existir ou tiver expirado).

Skill em foco: DOM, fetch/promises/async-await, eventos JS, CSS responsivo.

FASE 4 — CSS e polimento do website (Semana 5-6)
 Definir paleta e tipografia (podes reaproveitar o estilo do Enunciado.docx — azul/rosa/verde).
 Layout responsivo (grid/flexbox) para listagem de veículos tipo "cards".
 Estados de loading/erro visíveis ao utilizador.

Skill em foco: CSS Grid/Flexbox, design de interface.

FASE 5 — App Desktop: gestão de frota (Semana 6-7)
 api_client.py: wrapper com requests para GET/POST/PUT/DELETE à API (reaproveita o token de staff).
 Janela de login.
 Janela "Veículos" (listar, registar, alterar, remover, marcar em manutenção).
 Janela "Clientes" e "Reservas" (listar/pesquisar).
 Dashboard inicial: veículos alugados, últimos clientes, veículos por categoria, reservas do mês + total financeiro, alertas de revisão/inspeção a expirar.
 Exportação para CSV (usa csv da standard library — simples e cumpre o critério técnico).

Skill em foco: Tkinter, consumo de API a partir de Python, csv/pandas básico para exportação.

FASE 6 — Deploy na AWS Free Tier (Semana 7-8)
 Criar conta AWS Free Tier, configurar billing alerts (importante — para não teres surpresas).
 RDS PostgreSQL free tier — migrar de SQLite (SQLAlchemy torna isto quase indolor).
 EC2 (t2.micro/t3.micro) — deploy da API Flask com Gunicorn + Nginx.
 S3 — guardar imagens dos veículos em vez de ficheiros locais.
 Documentar cada passo em docs/DEPLOY_AWS.md (screenshots + comandos) — isto por si só é ótimo material de defesa.

Skill em foco: AWS EC2/RDS/S3, deployment básico, Nginx/Gunicorn.

FASE 7 (extensão, se houver tempo) — Polimento final
 Gráficos no dashboard (Tkinter com matplotlib embutido, ou o website com Chart.js).
 Melhorar segurança (rate limiting, validação mais robusta).
 Rever toda a documentação e preparar guião de defesa (perguntas prováveis + respostas).
7. Recursos de aprendizagem por tecnologia
Python/Flask REST APIs: documentação oficial do Flask (flask.palletsprojects.com) + Flask-SQLAlchemy docs.
JavaScript (fetch, DOM, async): MDN Web Docs (developer.mozilla.org) — é a referência que qualquer programador júnior deve saber navegar.
SQL/SQLAlchemy: já tens o módulo 5 exercício 4 do curso como base.
AWS Free Tier: a página que já tens (aws.amazon.com/free) + a documentação de "Getting Started" da EC2 e RDS.
Tkinter: documentação oficial do Python (docs.python.org/3/library/tkinter.html).
8. Como vamos trabalhar juntos

A cada sessão (30-60 min), diz-me em que Fase/tarefa estás e eu:

Explico o conceito necessário para essa mini-tarefa (sem te dar só código para copiar — para dominares na defesa).
Reviso o teu código quando o colares ou anexares.
Atualizo contigo a documentação relevante em docs/.

Não precisas de seguir a ordem à risca — se um dia só tiveres energia para "só JS" ou "só desenhar BD", dizes-me e ajusto.

FASE 7 (extensão) — Sistema de recomendação + polimento
 Sistema de recomendação "veículos semelhantes" na página de detalhe: scikit-learn,
   k-nearest neighbors sobre categoria/preço/capacidade. Endpoint novo GET /api/veiculos/<id>/similares,
   cálculo feito inteiramente no backend; o frontend só recebe e apresenta a lista.
 Gráficos no dashboard (Tkinter com matplotlib, ou Chart.js no website).
 Rever documentação e preparar guião de defesa.

 FASE 8 (extensão comercial, pós-MVP) — Maturidade "chave-na-mão"
 Login/registo via Google OAuth, adicional ao login por email/password já existente.
 Página de gestão de métodos de pagamento: cliente regista cartão/MB Way antes de reservar; a reserva passa a escolher entre métodos já guardados, com um predefinido.
 Simulação de validação (limite de cartão fictício, "comunicação" simulada com MB Way) — sem gateway real, mantendo a decisão já registada de não processar pagamentos verdadeiros.
 Emails transacionais (confirmação de reserva, recuperação de password) via SMTP/API, usando a conta luxurywheelspedroserrano@gmail.com — credenciais sempre em .env, nunca no código.
  (nice to have) Mostrar datas já reservadas na página do veículo, para o cliente não escolher um período indisponível às cegas — versão simples: lista de intervalos reservados por baixo do formulário; versão completa: calendário próprio com dias desativados.

FASE 3 (continuação) — Refinamentos identificados ao testar "Minhas Reservas"

O backend dos estados calculados (Reservada/Ativa/Concluída/Cancelada) já está feito e protegido (ver DECISOES.md). Falta o frontend acompanhar:

 Trocar a condição única `if (reserva.estado === 'Ativa')` em reservas.js por duas condições separadas: botão "Cancelar" só quando o estado calculado for 'Reservada', botão "Alterar" só quando for 'Ativa'.
 Construir a UI do botão "Alterar": input de nova data_fim + função alterarReserva(reservaId, novaDataFim) em api.js (PUT /api/reservas/<id>, já existe e já está protegido no backend).
 Layout em tabela para "Minhas Reservas" em vez dos cartões atuais: colunas Matrícula | Marca | Modelo | Data Início | Data Fim | Valor Total | Estado | [Cancelar] | [Alterar] (as duas últimas colunas sem cabeçalho).
 Filtro e ordenação da tabela (nem que seja só por estado, para começar).
 Deteção proativa de sessão expirada: hoje, o navbar.js só verifica se existe um token no localStorage, não se ainda é válido — por isso um utilizador com token expirado continua a ver-se como autenticado até tentar fazer alguma ação. Descodificar o campo exp do JWT (é só Base64, sem biblioteca nenhuma) e comparar com a hora atual permite detetar isto mais cedo e fazer logout automático. Importante para a defesa: isto é só para a experiência do utilizador, a validação a sério continua sempre a acontecer no backend.

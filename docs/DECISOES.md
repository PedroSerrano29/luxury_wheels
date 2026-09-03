# Registo de Decisões de Arquitetura — Luxury Wheels

> Cada entrada documenta uma decisão técnica não trivial: o contexto que a motivou, as alternativas consideradas, a escolha final, e a justificação. Serve como referência rápida durante a defesa de tese.

---

## Arquitetura geral: API REST central + dois clientes

**Contexto:** o projeto exige um website (Proposta A) e uma aplicação desktop de gestão de frota (Proposta B).

**Alternativas consideradas:** (1) Flask a renderizar HTML diretamente com Jinja2 para o website, e o Tkinter a aceder à base de dados diretamente; (2) uma API REST central em Flask, consumida por ambos os clientes.

**Escolha:** API REST central (Flask + SQLAlchemy) que devolve JSON; o website (HTML/CSS/JavaScript) e a app desktop (Tkinter) são ambos clientes independentes que consomem essa API.

**Justificação:** evita duplicar regras de negócio em dois sítios (ex: "veículo fica indisponível após reserva" vive só no backend); prepara o sistema para escalar (ex: uma futura app mobile usaria a mesma API sem alterações); separa claramente apresentação de lógica de negócio.

---

## Autenticação: JWT em vez de sessões Flask

**Contexto:** tanto o website como a app desktop precisam de autenticar-se na mesma API.

**Alternativas consideradas:** sessões Flask (cookies), JSON Web Tokens (JWT).

**Escolha:** JWT, com o token enviado no cabeçalho `Authorization` de cada pedido.

**Justificação:** a app desktop não é um browser e não gere cookies facilmente; um token enviado no header funciona de forma idêntica para os dois clientes. `cliente_id`/`utilizador_id` e `role` vão codificados no próprio token, assinado com uma `SECRET_KEY` guardada em `.env`.

**Trade-off aceite:** tokens com validade fixa de 24h, sem mecanismo de refresh — aceitável para o âmbito do projeto.

---

## Dois tipos de conta, dois endpoints de login

**Contexto:** clientes (que alugam veículos) e staff (gestores/admins que gerem a frota) têm permissões e propósitos completamente diferentes.

**Escolha:** duas tabelas separadas (`clientes` e `utilizadores`) e dois endpoints de autenticação (`POST /api/auth/login` e `POST /api/auth/login-staff`), cada um a gerar um token com claims diferentes (`cliente_id` vs. `utilizador_id` + `role`).

**Justificação:** reflete a separação real do negócio; permite aplicar autorização por `role` (`gestor`/`admin`) só onde faz sentido, sem misturar conceitos numa tabela genérica de "utilizadores".

**Nota de segurança:** não existe endpoint público de registo de staff — a primeira conta admin é criada manualmente na base de dados pelo próprio dono do sistema, para evitar que qualquer pessoa se possa auto-registar com permissões de gestão.

---

## `cliente_id` vem sempre do token, nunca do corpo do pedido

**Contexto:** ao criar uma reserva ou consultar o histórico, é preciso saber a que cliente essa ação pertence.

**Risco identificado:** se o `cliente_id` fosse aceite diretamente no JSON enviado pelo cliente, qualquer pessoa autenticada poderia criar reservas ou ver histórico de outro cliente qualquer, só alterando esse número.

**Escolha:** `cliente_id` é sempre extraído do token JWT validado (via decorator `token_obrigatorio`), nunca de `request.get_json()`. O mesmo princípio aplica-se à verificação de posse em `PUT /api/reservas/<id>` — compara-se o `cliente_id` do token com o dono real da reserva antes de qualquer alteração.

---

## Exclusão de dados sensíveis e segredos do controlo de versão

**Contexto:** o projeto lida com dados de clientes (mesmo que fictícios em desenvolvimento) e precisa de credenciais reais (AWS, `SECRET_KEY`) nas fases seguintes.

**Escolha:** `.gitignore` exclui bases de dados (`*.db`), ambiente virtual (`venv/`) e ficheiros `.env`; criado `.env.example` como documentação da estrutura de configuração sem expor valores reais.

**Justificação:** replica prática padrão da indústria — dados e segredos nunca em repositórios de código, mesmo privados. Um segredo commitado uma única vez fica no histórico do Git permanentemente, mesmo que apagado depois.

---

## Duas taxonomias de categoria numa só coluna, dependendo do tipo de veículo

**Contexto:** o enunciado define categorias `Pequeno/Médio/Grande/SUV/Luxo` para a pesquisa de veículos, mas esta taxonomia não faz sentido para motas.

**Escolha:** a coluna `categoria` mantém-se única na tabela `veiculos`, mas o seu significado depende do `tipo`: carros usam a taxonomia do enunciado; motas usam `Naked/Scooter/Touring` (mais realista e útil para o cliente). O `seed.py` aplica esta lógica de mapeamento na importação do CSV original.

**Critério para `Luxo`:** carros não-SUV com `valor_diaria` ≥ 90€/dia (regra definida por ausência de indicação explícita no CSV de origem).

**Consequência no frontend:** o filtro de categoria no website mostra opções diferentes consoante o `tipo` selecionado — um filtro dependente/condicional, padrão comum em e-commerce (ex: Amazon muda opções de tamanho consoante a categoria de produto escolhida).

---

## Soft delete + hard delete híbrido para veículos

**Contexto:** é preciso poder retirar um veículo da frota (ex: foi vendido), mas sem perder o histórico de reservas associadas a ele.

**Escolha:** dois mecanismos distintos:
- **Soft delete** (`PUT /api/veiculos/<id>/desativar`): marca `ativo=False` e `disponivel=False`, sem apagar o registo. Acessível a gestores e admins.
- **Hard delete** (`DELETE /api/veiculos/<id>`): apaga fisicamente o registo, mas só é permitido se não existirem reservas associadas (devolve `409 Conflict` caso contrário). Reservado a admins.

**Justificação:** protege a integridade do histórico no dia a dia, mas mantém uma via de limpeza definitiva para dados verdadeiramente descartáveis, sem comprometer a rastreabilidade de negócio.

---

## Âmbito de pagamento: sem processamento real

**Contexto:** o enunciado pede "escolher forma de pagamento" durante a reserva.

**Escolha:** a tabela `formas_pagamento` guarda apenas o método preferido do cliente (ex: "Cartão", "MB Way"); não existe integração com nenhum gateway de pagamento real, nem validação de saldo/limite de crédito.

**Justificação:** processar pagamentos reais implicaria integração com um gateway (Stripe, SIBS, etc.), ambiente sandbox, e conformidade regulatória — fora do âmbito de um projeto académico. O sistema simula a escolha do método sem processar a transação.

---

## CORS aberto em desenvolvimento

**Contexto:** o website (servido em `127.0.0.1:8000`) e a API (`127.0.0.1:5000`) correm em portas diferentes: o browser trata isto como origens diferentes e bloqueia pedidos entre si por defeito (política de CORS).

**Escolha:** `flask-cors` configurado com `CORS(app)`, sem restrição de origem, apenas em ambiente de desenvolvimento.

**Nota para produção (Fase 6):** em AWS, a configuração deve restringir `Access-Control-Allow-Origin` só ao domínio real do website, nunca "qualquer origem".

---

## Manipulação do DOM via `createElement`/`textContent`, não `innerHTML`

**Contexto:** o frontend precisa de gerar HTML dinamicamente a partir de dados vindos da API (cartões de veículos, campos de filtro).

**Alternativas consideradas:** `innerHTML` com template literals (mais rápido de escrever); `document.createElement()` + `textContent` (mais verboso).

**Escolha:** `createElement`/`textContent` em toda a geração dinâmica de HTML.

**Justificação:** `textContent` nunca interpreta o conteúdo como HTML executável, prevenindo ataques XSS caso o valor inserido venha de dados de utilizador (nomes, comentários, etc.) — mesmo que o risco atual seja baixo com dados só de veículos, o hábito protege automaticamente quando o projeto passar a mostrar dados de clientes. Trade-off consciente: mais código do que `innerHTML`, em troca de segurança e controlo explícitos.

---

## Copywriting orientado a conversão nos títulos de página

**Contexto:** o título da página de listagem de veículos.

**Escolha:** "Escolha o seu Luxo sobre Rodas" em vez de "Veículos Disponíveis".

**Justificação:** "Disponíveis" sugere implicitamente um inventário limitado/escasso a um visitante que ainda não fez login; a frase aspiracional convida à ação sem essa conotação — uma consideração de marketing/UX, não só de copy genérico.

---

## Nota técnica: duplicação de código intencional (candidato a refactor)

Existe pequena duplicação entre `buscarVeiculos()` (sem filtros) e a lógica de fetch dentro de `aplicarFiltro()` (com filtros) em `filtros.js`. Mantido assim deliberadamente por simplicidade nesta fase; candidato a unificação futura (`buscarVeiculos(filtros = {})` com parâmetro opcional).


## Regras de reservas centralizadas em serviços

**Contexto:** a validação das datas e a deteção de conflitos de reservas eram repetidas nos endpoints de criação e alteração.

**Alternativas consideradas:** manter a lógica diretamente em cada rota Flask; ou extrair a lógica de negócio para um módulo de serviços reutilizável.

**Escolha:** criar `backend/services/reservas_service.py`, com funções independentes de HTTP para validar datas e verificar a disponibilidade de um veículo num período.

**Justificação:** evita duplicação de código, mantém as regras de negócio no backend Python e permite reutilizar a mesma lógica em futuros endpoints, na aplicação desktop e em testes automatizados.

## Âmbito alargado: Proposta A + Proposta B + Machine Learning

**Contexto:** o enunciado pede a escolha de uma proposta (A ou B); decidi implementar a Proposta A
como núcleo do projeto e adicionar a Proposta B como extensão comercial ("solução chave-na-mão"),
mais um módulo de recomendação com scikit-learn (Fase 7).

**Justificação:** ambas as propostas consomem a mesma API REST central, sem duplicar regras de
negócio; o módulo de recomendação demonstra aplicação prática de ML supervisionado/não supervisionado
sem sair do âmbito Python do curso, e aumenta o valor comercial percebido do produto final.

## Âmbito comercial: funcionalidades de maturidade adiadas para depois do MVP

**Contexto:** ao construir o formulário de reserva, ficou claro que uma versão "chave-na-mão" precisa de mais do que o enunciado pede: login social (Google), métodos de pagamento pré-registados e validados (não escolhidos de novo a cada reserva), e emails transacionais (confirmação de reserva, recuperação de password) — já existe uma conta de email dedicada (`luxurywheelspedroserrano@gmail.com`) reservada para isto.

**Escolha:** manter o MVP atual (forma de pagamento escolhida por tipo, criada/reaproveitada na hora) como base funcional dentro do prazo do curso, e registar estas funcionalidades como Fase 8 do roadmap, a implementar depois de Propostas A+B+ML estarem concluídas e testadas.

**Justificação:** o prazo do curso não permite integrar OAuth, envio de emails e simulação de validação de pagamento sem comprometer o essencial exigido no enunciado. Documentar esta visão comercial mostra maturidade de produto na defesa de tese, sem arriscar o prazo de entrega.

---

## Rotas de gestão de veículos protegidas por autenticação e role

**Contexto:** `POST/PUT /api/veiculos` e `PUT /api/veiculos/<id>/desativar` não tinham nenhuma proteção — qualquer pedido, sem sessão nenhuma, conseguia criar, alterar ou desativar veículos da frota. Só o `DELETE` (hard delete) já estava protegido.

**Escolha:** as três rotas passaram a exigir `@token_obrigatorio` e a verificar `dados.get('role') in ('gestor', 'admin')` — o mesmo padrão já usado no `DELETE`, mas menos restritivo (gestor ou admin, não só admin), porque gerir o dia a dia da frota deve estar acessível aos gestores.

**Justificação:** corrige uma falha de segurança real, e alinha esta parte da API com a decisão já registada de que a gestão da frota é uma operação de staff (Proposta B), nunca acessível a um cliente comum ou a um visitante não autenticado.

---

## Forma de pagamento resolvida pelo tipo, não pelo id, no momento da reserva

**Contexto:** a tabela `formas_pagamento` já existia no modelo de dados, mas não havia nenhuma rota nem ecrã para o cliente registar previamente um método de pagamento — e a criação de reserva exige um `forma_pagamento_id` válido (chave estrangeira obrigatória). Construir primeiro um ecrã completo de gestão de métodos de pagamento (adiado para a Fase 8) bloquearia todo o fluxo de reserva.

**Alternativas consideradas:** (1) exigir do frontend um `forma_pagamento_id` já existente, o que implicava construir a gestão de métodos de pagamento antes de conseguir reservar seja o que for; (2) o cliente escolhe só o *tipo* (`"Cartão"`, `"MB Way"`) no próprio formulário de reserva, e o backend resolve ou cria a linha correspondente.

**Escolha:** o frontend envia `forma_pagamento_tipo` (uma string); a rota `criar_reserva` chama `obter_ou_criar_forma_pagamento(cliente_id, tipo)` (em `backend/services/pagamentos_service.py`), que procura uma `FormaPagamento` existente para aquele cliente e tipo, e só cria uma nova se não existir. Usa `db.session.flush()` (não `commit()`) para obter o `id` da forma de pagamento nova de imediato, sem fechar a transação — o `commit()` definitivo só acontece depois, junto com a criação da própria reserva, para que as duas operações sejam atómicas (ou ambas são gravadas, ou nenhuma é).

**Justificação:** desbloqueia o fluxo de reserva sem depender da Fase 8 estar pronta, evita duplicar linhas de `formas_pagamento` para o mesmo cliente e tipo, e mantém a lógica no backend — o frontend nunca decide nem inventa nenhum `id`.

---

## Estados de reserva calculados a partir das datas, não gravados como valor fixo

**Contexto:** o campo `estado` de uma `Reserva` só distinguia `'Ativa'`/`'Cancelada'`, definido manualmente em cada ação. Isto não refletia se uma reserva já tinha terminado (`data_fim` no passado), nem impedia ações que já não faziam sentido — por exemplo, cancelar uma reserva que já estava a decorrer, ou alterar as datas de uma que ainda nem tinha começado.

**Alternativas consideradas:** (1) manter `estado` como campo simples, atualizado por uma tarefa periódica (scheduler/cron) que percorre as reservas e as atualiza; (2) calcular o estado dinamicamente, sempre que é pedido, comparando as datas gravadas com a data de hoje — sem processo nenhum a correr em segundo plano.

**Escolha:** um método `calcular_estado()` no modelo `Reserva` (`backend/models.py`). Se o campo `estado` gravado for `'Cancelada'`, devolve isso diretamente — é a única transição manual que continua a existir. Caso contrário, deriva o estado comparando `date.today()` com o período da reserva: `'Reservada'` (hoje ainda não chegou à `data_inicio`), `'Ativa'` (hoje está dentro do período, incluindo o próprio dia de `data_fim`), ou `'Concluída'` (já passou a `data_fim`). O `to_dict()` expõe sempre este valor calculado — nunca o campo em bruto — por isso nenhum consumidor da API (frontend do website, ou futuramente o dashboard da app desktop) precisa de saber que este cálculo existe.

**Justificação:** sem precisar de nenhum scheduler, o estado está sempre correto em qualquer pedido à API, por mais tempo que passe sem ninguém mexer na reserva. A mesma lógica vai ser reutilizada tal e qual no dashboard da Proposta B, para agregações por estado (reservas ativas, concluídas do mês, etc.).

---

## Regras de cancelar/alterar reserva ligadas ao estado calculado, aplicadas no backend

**Contexto:** com os estados calculados definidos, foi preciso decidir em que momento do ciclo de vida de uma reserva cada ação é permitida.

**Escolha:** só é possível **cancelar** uma reserva no estado `'Reservada'` (antes de começar). Só é possível **alterar** — e só a `data_fim`, nunca a `data_inicio` — de uma reserva no estado `'Ativa'`, e a nova `data_fim` nunca pode ser anterior a hoje. Ambas as regras são verificadas dentro da rota `PUT /api/reservas/<id>`, devolvendo `409 Conflict` quando violadas — não são só uma condição a esconder um botão no frontend.

**Justificação:** esconder um botão no frontend é só conveniência de interface; sem a verificação replicada no backend, um pedido direto à API (`curl`, Postman) continuaria a conseguir cancelar uma reserva a decorrer ou alterar datas de uma já concluída. Reforça, mais uma vez, o princípio seguido desde o início: o backend decide, o frontend só mostra e recolhe input. Testado manualmente com `curl` para os três casos (cancelar Ativa → bloqueado; alterar datas de Reservada → bloqueado; alterar `data_fim` de Ativa → sucesso, com recálculo correto do `valor_total`).

---

## Componentes de DOM partilhados entre páginas (`dom-utils.js`)

**Contexto:** a função `criarLinha(rotulo, valor)` (gera um parágrafo `"Rótulo: valor"`) foi escrita para a página de detalhe do veículo, mas a página "Minhas Reservas" precisava exatamente da mesma coisa.

**Escolha:** extraída para um ficheiro novo, `web_app/static/js/dom-utils.js`, incluído em qualquer página HTML que precise de construir este tipo de linha — hoje `veiculo.html` e `minhas-reservas.html`. `api.js` mantém-se reservado só para funções `fetch()`, como já estava documentado; helpers de construção de DOM ficam à parte.

**Justificação:** evita duplicar a mesma função em dois ficheiros `.js` — o mesmo princípio DRY já aplicado ao `filtros.js` (reaproveitado para o `<select>` de forma de pagamento no formulário de reserva).

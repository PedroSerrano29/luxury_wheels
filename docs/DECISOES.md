## Decisão: Exclusão de dados sensíveis e segredos do controlo de versão
**Contexto:** o projeto lida com dados de clientes (mesmo que fictícios em desenvolvimento)
e vai precisar de credenciais AWS reais na fase de deploy.
**Escolha:** .gitignore exclui bases de dados (*.db) e ficheiros .env; criado .env.example
como documentação da estrutura de configuração sem expor valores.
**Justificação:** replica prática padrão da indústria — dados e segredos nunca em
repositórios de código, mesmo privados.

## Decisão: Duas taxonomias de categoria numa só coluna, dependendo do tipo de veículo
**Contexto:** o enunciado define categorias 'Pequeno/Médio/Grande/SUV/Luxo' para a pesquisa
de veículos, mas isto não faz sentido para motas.
**Escolha:** a coluna `categoria` mantém-se única na tabela `veiculos`, mas o seu significado
depende do `tipo`: carros usam a taxonomia do enunciado; motas usam `Naked/Scooter/Touring`
(mais realista e útil para o cliente). O `seed.py` aplica esta lógica na importação.
**Consequência no frontend:** o filtro de categoria no website terá de mostrar opções
diferentes consoante o `tipo` selecionado (filtro dependente).
**Critério para 'Luxo':** carros não-SUV com valor_diaria ≥ 90€/dia.
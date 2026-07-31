## Decisão: Exclusão de dados sensíveis e segredos do controlo de versão
**Contexto:** o projeto lida com dados de clientes (mesmo que fictícios em desenvolvimento)
e vai precisar de credenciais AWS reais na fase de deploy.
**Escolha:** .gitignore exclui bases de dados (*.db) e ficheiros .env; criado .env.example
como documentação da estrutura de configuração sem expor valores.
**Justificação:** replica prática padrão da indústria — dados e segredos nunca em
repositórios de código, mesmo privados.
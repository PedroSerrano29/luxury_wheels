Ativar ambiente virtual:
source venv/bin/activate

rm luxury_wheels.db - remove a base de dados
sqlite3 luxury_wheels.db < schema.sql - Cria a base de dados com sqlite3 atraves do schema.sql

Criar variaveis aleatorias com python
python3 -c "import secrets; print(secrets.token_hex(32))
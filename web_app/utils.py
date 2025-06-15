def apply_filter(query, field, value):
    """
    Aplica um filtro a uma query SQLAlchemy se o valor for fornecido.

    Parâmetros:
        query (Query): A query SQLAlchemy onde o filtro será aplicado.
        field (str): O nome do campo a ser filtrado.
        value (str): O valor a ser usado no filtro.

    Retorna:
        Query: A query com o filtro aplicado, ou a query original se o valor não for fornecido.

    Exemplo:
        query = session.query(Veiculo)
        query = apply_filter(query, 'categoria', 'SUV')
    """
    if not query:
        raise ValueError("A query não pode ser None.")
    if not field:
        raise ValueError("O campo (field) não pode ser None.")

    if value:
        return query.filter_by(**{field: value})
    return query
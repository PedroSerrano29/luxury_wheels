from models import db, FormaPagamento

def obter_ou_criar_forma_pagamento(cliente_id, tipo):
    forma = FormaPagamento.query.filter_by(cliente_id=cliente_id, tipo=tipo).first()

    if forma is None:
        forma = FormaPagamento(cliente_id=cliente_id, tipo=tipo)
        db.session.add(forma)
        db.session.flush()

    return forma
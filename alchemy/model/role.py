from extensions import db

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # Essa linha define um relacionamento entre as tabelas Role e User
    # - db.relationship() cria uma relação com a tabela User
    # - 'User' é o nome da classe/modelo que será relacionada
    # - backref='role' cria automaticamente uma propriedade 'role' na classe User
    #   que permite acessar o Role associado a partir de um objeto User
    # - users será uma lista de objetos User associados a este Role
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

from extensions import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # role_id é uma coluna que armazena o ID do Role associado a este usuário
    # - db.Column() define uma coluna na tabela
    # - db.Integer especifica que é uma coluna de números inteiros
    # - db.ForeignKey('roles.id') cria uma chave estrangeira que referencia
    #   a coluna 'id' da tabela 'roles', estabelecendo o relacionamento
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User %r>' % self.username


from flask import Flask, jsonify, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
#from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String

# A classe Base serve como uma classe base declarativa para os modelos SQLAlchemy
# Ela herda de DeclarativeBase que fornece a funcionalidade necessária para 
# definir modelos/tabelas do banco de dados de forma declarativa
# Ao passar essa classe Base como model_class para SQLAlchemy,
# todos os modelos que herdam de db.Model terão essa base declarativa
class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)


# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# initialize the app with the extension
db.init_app(app)
#migrate = Migrate(app, db)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str]


with app.app_context():
    db.create_all()


@app.route("/users")
def user_list():
    # O método scalars() é usado para retornar apenas os objetos User diretamente,
    # ao invés de tuplas com uma única coluna contendo o objeto User.
    # Sem o scalars(), o resultado seria uma lista de tuplas como [(user1,), (user2,)]
    # Com scalars(), obtemos diretamente [user1, user2]
    users = db.session.execute(db.select(User).order_by(User.id.desc())).scalars()
    return jsonify([{
        "id": user.id, 
        "username": user.username, 
        "email": user.email,
        "lastname": user.lastname
    } for user in users])

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            lastname=request.form["lastname"]
        )
        db.session.add(user)
        db.session.commit()
        return jsonify({
            "message": "User created", 
            "user": {
                "id": user.id, 
                "username": user.username, 
                "email": user.email,
                "lastname": user.lastname
            }
        })

    return jsonify({"message": "Use POST method to create user"})

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return jsonify({
        "id": user.id, 
        "username": user.username, 
        "email": user.email,
        "lastname": user.lastname
    })

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            "message": "User deleted", 
            "user": {
                "id": user.id, 
                "username": user.username, 
                "email": user.email,
                "lastname": user.lastname
            }
        })

    return jsonify({
        "message": "Use POST method to delete user", 
        "user": {
            "id": user.id, 
            "username": user.username, 
            "email": user.email,
            "lastname": user.lastname
        }
    })


@app.route("/select")
def select():
    # O método json é usado para obter o valor do campo id da requisição
    id = request.json.get('id')
    # O método args é usado para obter o valor do campo id da requisição
    #id = request.args.get('id')
    #users = db.session.execute(db.select("SELECT * FROM users where username = 'john'")).scalars()
    #users = db.session.execute(db.select(User).where(User.username.in_(['a']))).scalars()
    #users = db.session.execute(db.select(User).where(User.username.like('%a%'))).scalars()
    users = db.session.execute(db.select(User).where(User.lastname != None)).scalars()
    app.logger.info(f'users: {(users)}')
    return jsonify([{
        "id": user.id, 
        "username": user.username, 
        "email": user.email,
        "lastname": user.lastname
    } for user in users])

if __name__ == "__main__":
    app.run(debug=True)


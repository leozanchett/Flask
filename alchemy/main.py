import os
from flask import Flask, jsonify
from extensions import db
from model.role import Role
from model.user import User
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

with app.app_context():
    db.drop_all()
    db.create_all()
    admin_role = Role(name='Admin')
    mod_role = Role(name='Moderator')
    user_role = Role(name='User')

    user_john = User(username='john', role=admin_role)
    user_susan = User(username='susan', role=user_role)
    user_david = User(username='david', role=mod_role)

    db.session.add_all([admin_role, mod_role, user_role, user_john, user_susan, user_david])
    db.session.commit()

@app.route('/user/<username>')
def get_user(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            'username': user.username,
            'role': user.role.name
        })
    
    user_role = Role.query.filter_by(name='User').first()
    new_user = User(username=username, role=user_role)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        'username': new_user.username,
        'role': new_user.role.name
    })

@app.shell_context_processor
def make_shell_context():
    return dict(app=app, db=db, Role=Role, User=User)


if __name__ == '__main__':
    app.run(debug=True)



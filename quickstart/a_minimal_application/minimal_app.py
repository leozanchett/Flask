# from flask import Flask, url_for
# from markupsafe import escape

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return 'index'

# @app.route('/login/')
# def login():
#     return 'login'

# @app.route('/user/<username>')
# def profile(username):
#     return f'{username}\'s profile'

# with app.test_request_context():
#     print(url_for('index'))
#     print(url_for('login'))
#     print(url_for('login', next='/'))
#     print(url_for('profile', username='John Doe'))

from flask import Flask, url_for

app = Flask(__name__)

@app.route('/user/<username>/')
@app.route('/user/<username>/<int:post_id>')
def profile(username, post_id = None):
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    if post_id is not None:
        return f'Perfil do usuário {username} com post {post_id}'
    else:
        return f'Perfil do usuário {username}'

with app.test_request_context():
    pass
    #url_for('profile', username='joao')
    #print(url_for('profile', username='joao', _external=True))
    #print(url_for('profile', username='joao', post_id=42, _external=True))
    # Saída: /user/joao
    # Saída: /user/joao/42

from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def hello():
    return "<h1>Hello, World!</h1>"

@app.route("/name/<name>")
def name(name):
    return f"Hello, {name}!"

@app.route("/user_agent")
def user_agent():
    user_agent = request.headers.get("User-Agent")
    return f"Your browser is {user_agent}"

@app.route("/request_object")
def request_object():
    json_object = {
        "method": request.method,
        "url": request.url,
        "headers": dict(request.headers),
        "is_secure": request.is_secure,
        "scheme": request.scheme,
        "full_path": request.full_path,
        "path": request.path,
        "query_string": request.query_string.decode(),
        "remote_addr": request.remote_addr,
        "user_agent": request.user_agent,
    }
    # Só tenta pegar o JSON se o Content-Type for application/json
    if request.is_json:
        json_object["body"] = request.get_json()
    else:
        json_object["body"] = None
        
    return jsonify(json_object)


#if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)


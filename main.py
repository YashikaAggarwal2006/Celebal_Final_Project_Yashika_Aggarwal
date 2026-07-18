# main.py
#
# WHAT THIS FILE DOES:
# This is the file you actually run (python main.py).
# It creates the Flask app, connects the routes from routes.py,
# and starts the local web server.

from flask import Flask
from routes import routes

app = Flask(__name__)
app.register_blueprint(routes)

if __name__ == "__main__":
    # debug=True auto-reloads the server when you edit code -- handy while learning
    app.run(debug=True, port=5000)

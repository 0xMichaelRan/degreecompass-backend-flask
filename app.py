from flask import Flask
from routes.major_routes import major_bp

app = Flask(__name__)
app.register_blueprint(major_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)

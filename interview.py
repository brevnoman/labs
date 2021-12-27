from mainapp import app
from mainapp.middleware import Middleware

if __name__ == "__main__":
    app.wsgi_app = Middleware(app.wsgi_app)
    app.run("0.0.0.0", 5000)

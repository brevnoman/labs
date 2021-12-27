class Middleware:

    def __init__(self, app):
        print("I tut")
        self.app = app

    def __call__(self, environ, start_response):
        print("ya tut bil")
        return self.app(environ, start_response)

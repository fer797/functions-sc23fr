import logging
import flask
import azure.functions as func

app = flask.Flask(__name__)

@app.route('/')
def index():
    return "Hello from Flask!"

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    return func.WsgiMiddleware(app.wsgi_app).handle(req, context)

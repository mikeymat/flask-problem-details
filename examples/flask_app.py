from flask import Flask
from flask_problem_details import configure_app, from_exception
from werkzeug.exceptions import NotImplemented

flask_builder : Flask = lambda args: Flask(__name__)
app : Flask = configure_app(app_builder = flask_builder, with_traceback=True)

@app.get("/authors")
def get_authors():
    raise NotImplemented()

@app.get("/books")
def get_books():
    description: str = "The method is not implemented"
    extras : dict = {"one": "extra value"}
    raise from_exception(NotImplementedError(description), extras = extras)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
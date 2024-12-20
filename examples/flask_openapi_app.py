from flask_openapi3 import OpenAPI, Info
from flask_problem_details import configure_app, from_exception
from werkzeug.exceptions import NotImplemented

# OpenAPI information
info: Info = Info(title="Flask OpenAPI 3 Example", version="1.0.0")
openapi_builder : OpenAPI = lambda args : OpenAPI(__name__, info=info, **args)

app : OpenAPI = configure_app(app_builder = openapi_builder, with_traceback=True)

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
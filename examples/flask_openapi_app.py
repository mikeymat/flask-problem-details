from flask_openapi3 import OpenAPI, Info
from pydantic import BaseModel
from werkzeug.exceptions import NotImplemented
from typing import Callable

from flask_problem_details import configure_app, from_exception, ProblemDetails, ProblemDetailsError

# OpenAPI information
info: Info = Info(title="Flask OpenAPI 3 Example", version="1.0.0")
openapi_callback: Callable[[dict], OpenAPI] = lambda args : OpenAPI(__name__, info=info, **args)

app : OpenAPI = configure_app(app = openapi_callback, with_traceback=True)

@app.get("/authors")
def get_authors():
    raise NotImplemented()

@app.get("/books")
def get_books():
    description: str = "The method is not implemented"
    extras : dict = {"one": "extra value"}
    raise from_exception(NotImplementedError(description), extras = extras)

@app.get("/cats")
def get_cats():
    problem = ProblemDetails(status=412, title = "No shelter", type= "uri:localhost:noshelter")
    raise ProblemDetailsError(problem)

class DogsQuery(BaseModel):
    id: int

@app.get("/dogs")
def get_dogs(query: DogsQuery):
    return { "id": query.id }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
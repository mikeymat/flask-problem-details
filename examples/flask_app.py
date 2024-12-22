from flask import Flask
from werkzeug.exceptions import NotImplemented
from flask_problem_details import configure_app, from_exception, ProblemDetails, ProblemDetailsError

app : Flask = configure_app(Flask(__name__), with_traceback=True)

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
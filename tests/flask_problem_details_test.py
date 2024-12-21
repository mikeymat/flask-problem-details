import unittest
from flask import Flask
from flask_openapi3 import OpenAPI
from pydantic_core import ValidationError
from werkzeug.exceptions import BadRequest, InternalServerError
from pydantic import BaseModel

import flask_problem_details as problem

class TestFlaskProblemDetails(unittest.TestCase):

    def setUp(self):
        self.app = problem.configure_app(Flask(__name__))
        self.client = self.app.test_client()

    def test_activate_traceback(self):
        problem.activate_traceback()
        self.assertTrue(problem.WITH_TRACEBACK)

    def test_deactivate_traceback(self):
        problem.deactivate_traceback()
        self.assertFalse(problem.WITH_TRACEBACK)

    def test_handle_http_exception_without_traceback(self):
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        #create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise BadRequest("This is a bad request")
        response = self.client.get('/problem')

        #check the response status code
        self.assertEqual(response.status_code, 400)
        #check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_generic_exception_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented"}

        #create a route that raises an exception
        @self.app.route('/problem')
        def exception_route():
            raise Exception("The method is not implemented")
        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_problem_details_error_without_extras_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented"}

        #create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(Exception("The method is not implemented"))
        response = self.client.get('/problem')

        #check the response status code
        self.assertEqual(response.status_code, 500)
        #check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_problem_details_error_with_extras_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented", "custom_field": "custom_value"}

        # create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(Exception("The method is not implemented"), extras={"custom_field": "custom_value"})
        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json, payload)
    
    def test_handle_http_exception_with_traceback(self):
        #create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        #run trigger the problem details with a custom payload
        problem.activate_traceback()
        @self.app.route('/problem')
        def problem_route():
            raise BadRequest("This is a bad request")
        response = self.client.get('/problem')
        problem.deactivate_traceback()

        #check the response status code
        self.assertEqual(response.status_code, 400)
        #check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        #check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_generic_exception_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 500, "title": "InternalServerError", "detail": "This is a bad request"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()
        @self.app.route('/problem')
        def problem_route():
            raise Exception("This is a bad request")
        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_problem_details_error_without_extras_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(BadRequest("This is a bad request"))
        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_problem_details_error_with_extras_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request", "custom_field": "custom_value"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(BadRequest("This is a bad request"), extras={"custom_field": "custom_value"})
        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        self.assertEqual(response.json.get("custom_field"), payload.get("custom_field"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))


class TestFlaskOpenAPIProblemDetails(unittest.TestCase):

    def setUp(self):
        self.app = problem.configure_app(lambda args : OpenAPI(__name__, **args))
        self.client = self.app.test_client()

    def test_activate_traceback(self):
        problem.activate_traceback()
        self.assertTrue(problem.WITH_TRACEBACK)

    def test_deactivate_traceback(self):
        problem.deactivate_traceback()
        self.assertFalse(problem.WITH_TRACEBACK)

    def test_handle_http_exception_without_traceback(self):
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        # create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise BadRequest("This is a bad request")

        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_generic_exception_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented"}

        # create a route that raises an exception
        @self.app.route('/problem')
        def exception_route():
            raise Exception("The method is not implemented")

        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_problem_details_error_without_extras_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented"}

        # create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(Exception("The method is not implemented"))

        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_problem_details_error_with_extras_without_traceback(self):
        payload = {"status": 500, "title": "InternalServerError", "detail": "The method is not implemented",
                   "custom_field": "custom_value"}

        # create a route that raises a problem details error
        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(Exception("The method is not implemented"),
                                         extras={"custom_field": "custom_value"})

        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json, payload)

    def test_handle_validation_error_without_traceback(self):
        payload = {"status": 400, "title": "BadRequest", "detail": "Validation Failed! Error count: 1"}
        class TestModel(BaseModel):
            id: str
        # create a route that raises a problem details error
        @self.app.get('/problem')
        def problem_route(query: TestModel):
            return {}
        response = self.client.get('/problem')

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the errors
        self.assertTrue("errors" in response.json)
        self.assertTrue(isinstance(response.json.get("errors"), list))

    def test_handle_http_exception_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()

        @self.app.route('/problem')
        def problem_route():
            raise BadRequest("This is a bad request")

        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_generic_exception_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 500, "title": "InternalServerError", "detail": "This is a bad request"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()

        @self.app.route('/problem')
        def problem_route():
            raise Exception("This is a bad request")

        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 500)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_problem_details_error_without_extras_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()

        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(BadRequest("This is a bad request"))

        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_problem_details_error_with_extras_with_traceback(self):
        # create a problem details with a custom payload
        payload = {"status": 400, "title": "BadRequest", "detail": "This is a bad request",
                   "custom_field": "custom_value"}

        # run trigger the problem details with a custom payload
        problem.activate_traceback()

        @self.app.route('/problem')
        def problem_route():
            raise problem.from_exception(BadRequest("This is a bad request"), extras={"custom_field": "custom_value"})

        response = self.client.get('/problem')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        self.assertEqual(response.json.get("custom_field"), payload.get("custom_field"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))

    def test_handle_validation_error_with_traceback(self):
        payload = {"status": 400, "title": "BadRequest", "detail": "Validation Failed! Error count: 1"}
        class TestModel(BaseModel):
            id: int
        # create a route that raises a problem details error
        problem.activate_traceback()
        @self.app.get('/problem')
        def problem_route(query: TestModel):
            return {"query": query.id}
        response = self.client.get('/problem?id=string')
        problem.deactivate_traceback()

        # check the response status code
        self.assertEqual(response.status_code, 400)
        # check the response payload
        self.assertEqual(response.json.get("status"), payload.get("status"))
        self.assertEqual(response.json.get("title"), payload.get("title"))
        self.assertEqual(response.json.get("detail"), payload.get("detail"))
        # check the traceback
        self.assertTrue("traceback" in response.json)
        self.assertTrue(isinstance(response.json.get("traceback"), str))
        # check the errors
        self.assertTrue("errors" in response.json)
        self.assertTrue(isinstance(response.json.get("errors"), list))

class TestFromException(unittest.TestCase):

    def test_from_exception_creates_problem_details_error(self):
        exception = Exception("Test exception")
        problem_details_error = problem.from_exception(exception)
        self.assertEqual(problem_details_error.problem.status, InternalServerError.code)
        self.assertEqual(problem_details_error.problem.title, InternalServerError.__name__)
        self.assertEqual(problem_details_error.problem.detail, str(exception))

    def test_from_exception_with_http_exception(self):
        exception = BadRequest("Bad request")
        problem_details_error = problem.from_exception(exception)
        self.assertEqual(problem_details_error.problem.status, exception.code)
        self.assertEqual(problem_details_error.problem.title, exception.__class__.__name__)
        self.assertEqual(problem_details_error.problem.detail, exception.description)

    def test_from_exception_with_extras(self):
        exception = Exception("Test exception with extras")
        extras = {"custom_field": "custom_value"}
        problem_details_error = problem.from_exception(exception, extras)
        self.assertEqual(problem_details_error.problem.status, InternalServerError.code)
        self.assertEqual(problem_details_error.problem.title, InternalServerError.__name__)
        self.assertEqual(problem_details_error.problem.detail, str(exception))
        self.assertEqual(problem_details_error.problem.custom_field, "custom_value")

    def test_from_exception_with_validation_error(self):
        class TestModel(BaseModel):
            field: str

        try:
            # noinspection PyTypeChecker
            TestModel(field=None)
        except ValidationError as validation_error:
            problem_details_error = problem.from_exception(validation_error)
            self.assertEqual(problem_details_error.problem.status, InternalServerError.code)
            self.assertEqual(problem_details_error.problem.title, InternalServerError.__name__)
            self.assertEqual(problem_details_error.problem.detail, str(validation_error))

if __name__ == '__main__':
    unittest.main()
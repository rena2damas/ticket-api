from flask_restful import Resource

from src import api


@api.resource('/test')
class Test(Resource):
    def get(self):
        """
        Example endpoint returning a list of colors by palette
        This is using docstrings for specifications.
        ---
        responses:
          200:
            description: Ok
        """
        return {'status': 'ok'}

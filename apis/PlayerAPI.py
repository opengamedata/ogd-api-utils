from flask_restful import Resource, Api

class PlayerAPI:
    @staticmethod
    def register(app):
        api = Api(app)
        api.add_resource(PlayerAPI.PlayerID, '/player/createID')

    class PlayerID(Resource):
        def get(self):
            return {
                "id":"FakePlayerID",
                "message":"Created a new fake player ID."
            }
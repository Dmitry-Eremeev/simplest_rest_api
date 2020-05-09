# Examples:

# curl -w "%{http_code}" -H 'Content-Type: application/json' http://localhost/version

# curl -w "%{http_code}" -d '{"name": "Mitya", "age": 33}' -H 'Content-Type: application/json' http://localhost/user

# curl -w "%{http_code}" -H 'Content-Type: application/json' http://localhost/user/278e8559-f5b7-4ae3-b609-544d1c031539

# curl -X DELETE -w "%{http_code}" -H 'Content-Type: application/json' \
# http://localhost/user/72e4424a-0c79-4a90-ae11-f80fb890ab79

from bottle import Bottle, request, response
from marshmallow import ValidationError

from main import User
from serialization import UserSchema

HOST = "localhost"
PORT = 8080
DEBUG = False

app = Bottle()
app.users = list()
user_schema = UserSchema()


@app.route('/version')
def version():
    return '{"version": "0.9"}'


@app.post('/user')
def create_user():
    try:
        app.users.append(User(**user_schema.load(request.json)))
        response.status = 201
        return user_schema.dumps(app.users[-1])
    except ValidationError as error:
        response.status = 400
        return {"error": str(error)}


@app.route('/user/<user_id>')
def get_user_info(user_id):
    for user in app.users:
        if user_id == user.id:
            return user_schema.dumps(user)
    response.status = 404


@app.delete('/user/<user_id>')
def delete_user(user_id):
    for user in app.users:
        if user_id == user.id:
            app.users.remove(user)
            response.status = 204
            return
    response.status = 404


app.run(host=HOST, port=PORT, debug=DEBUG)

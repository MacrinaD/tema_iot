from flask_restful import Resource, reqparse
from helper import UsersDatabase
from flask_jwt_extended import create_access_token, get_raw_jwt, jwt_required

from flask import jsonify, make_response

parser = reqparse.RequestParser()

parser.add_argument('username', help='This field cannot be blank', required=True)
parser.add_argument('password', help='This field cannot be blank', required=True)

blacklist = set()


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        if data['username'] in UsersDatabase.get_users().keys():
            if data['password'] == UsersDatabase.get_users()[data['username']]['password']:
                access_token = create_access_token(identity=data['username'])

                return jsonify({
                    "message": "Logged in successfully",
                    "access_token": access_token
                })

        return make_response(jsonify({
            "message": "Something went wrong"
        }), 400)


class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return make_response(jsonify({"msg": "Successfully logged out"}), 200)

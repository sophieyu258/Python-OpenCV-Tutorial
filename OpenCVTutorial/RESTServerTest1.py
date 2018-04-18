
#!/usr/bin/python3
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from json import dumps

app = Flask(__name__)
api = Api(app)


class Employees(Resource):
    def get(self):
        return {'employees': [888, 999, 1,2,3,4,5]} # Fetches first column that is Employee ID
    
    def post(self):
        """
        {
	"LastName":"micheal",
"FirstName":"jackson",
"Title":"CEO"
}
        """
        print(request.json)
        LastName = request.json['LastName']
        print(LastName)
        FirstName = request.json['FirstName']
        Title = request.json['Title']
        print(Title)

        return {'status':'success'}

    
class Tracks(Resource):
    def get(self):
        result = {'data': [(1,2), 'hello', [5,6,7]]}
        return jsonify(result)

    
class Employees_Name(Resource):
    def get(self, employee_id):
        result = {'data': ['hello', employee_id]}
        return jsonify(result)


api.add_resource(Employees, '/employees') # Route_1
api.add_resource(Tracks, '/tracks') # Route_2
api.add_resource(Employees_Name, '/employees/<employee_id>') # Route_3


if __name__ == '__main__':
     app.run()

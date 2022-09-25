from flask import Flask
from flask import request
from flask_restful import Api
from flask_cors import CORS #comment this on deployment

app = Flask(__name__)
CORS(app) #comment this on deployment
api = Api(app)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        username = request.json['username']
        return username
    return "Hello World!"

if __name__ == '__main__':
    app.run(debug=True)

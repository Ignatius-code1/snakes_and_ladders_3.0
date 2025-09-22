#from flask import Flask
#from flask_cors import CORS
#from flask_jwt_extended import JWTManager

#app = Flask(__name__)
#CORS(app)

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['JWT_SECRET_KEY'] = 'your-secret-key'

#db = SQLAlchemy(app)
#jwt = JWTManager(app)

#if __name__ == '__main__':
#    app.run(debug=True)

from flask_cors import CORS
CORS(app)
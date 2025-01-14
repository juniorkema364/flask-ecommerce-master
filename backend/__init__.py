from flask import Flask, config, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_cors import CORS

 

import os 

from backend .config import DevelopmentConfig , TestingConfig , ProductionConfig
 




db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()

login_manager.login_view = 'auth.login'   
login_manager.login_message = "Veuillez vous connecter pour accéder à cette page."




def create_app(config_class = DevelopmentConfig)  :
    app = Flask(__name__ , instance_relative_config= config_class)

    if os.getenv('FLASK_ENV') == "Development" :
        app.config['FLASK_ENV'] = DevelopmentConfig()
    elif os.getenv('FLASK_ENV') == "Production": 
        app.config['FLASK_ENV'] = ProductionConfig()
    elif os.getenv('FLASK_ENV') == "Testing" : 
        app.config['FLASK_ENV'] = TestingConfig()

    print('FLASK_ENV : ' , os.getenv('FLASK_ENV'))

    app.config.from_object(config_class)
    app.url_map.strict_slashes = False
    app.jinja_env.globals.update(zip=zip)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    CORS(app)

    from backend.auth.routes import auth 
    from backend.products.routes import products
    from backend.cart.routes import cart
    from backend.utils.user import main 

    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(cart)
    app.register_blueprint(main)

    with app.app_context(): 
        db.create_all()
        
        print('base de données crééer avec succes ')

    return app 
    
app = create_app()

frontend_folder = os.path.join(os.getcwd(),"..","frontend")
dist_folder = os.path.join(frontend_folder,"dist")






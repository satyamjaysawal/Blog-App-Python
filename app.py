from flask import Flask
from models import db, User  # Import User model to define user_loader
from flask_migrate import Migrate
from flask_login import LoginManager
from auth import auth as auth_blueprint
from routes import main as main_blueprint
from api import api as api_blueprint
from swagger import swaggerui_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'  # Set the login route

    # Initialize LoginManager with the app
    login_manager.init_app(app)

    # Define the user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(api_blueprint)
    app.register_blueprint(swaggerui_blueprint, url_prefix='/swagger')

    return app

# This is the part Flask will look for
app = create_app()

if __name__ == "__main__":
    import os
    port = os.environ.get('PORT', 5000)
    app.run(host='0.0.0.0', port=port)


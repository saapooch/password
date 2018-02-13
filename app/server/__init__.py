
import os

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app():

    # instantiate the app
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'app.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)


    # register blueprints
    from app.server.user.views import user_blueprint
    app.register_blueprint(user_blueprint)
    from app.server.account.views import account_blueprint
    app.register_blueprint(account_blueprint)

    # flask login
    from app.server.models import User
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(id):
        user = db.session.query(models.User).get(id)
        return user


    # error handlers
    # @app.errorhandler(401)
    # def unauthorized_page(error):
    #     return render_template('errors/401.html'), 401
    #
    # @app.errorhandler(403)
    # def forbidden_page(error):
    #     return render_template('errors/403.html'), 403
    #
    # @app.errorhandler(404)
    # def page_not_found(error):
    #     return render_template('errors/404.html'), 404
    #
    # @app.errorhandler(500)
    # def server_error_page(error):
    #     return render_template('errors/500.html'), 500

    return app

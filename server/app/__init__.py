from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from config import Config
from .errors import handle_exception


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    from .models import room, student_request, k_means_result
    
    from .controllers import main_api
    app.register_blueprint(main_api, url_prefix="/api")
    
    app.register_error_handler(Exception, handle_exception)
    
    return app
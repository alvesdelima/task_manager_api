from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

# Inicializa as extensões (mas ainda não as vincula ao app)
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=Config):
    """
    Fábrica de Aplicação: Cria e configura a instância do Flask.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Vincula as extensões à instância do app
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # -----------------------------------------------
    # Registrar os Blueprints (nossos endpoints)
    # -----------------------------------------------
    # Um Blueprint é um conjunto de rotas (ex: /auth/...)
    
    # Importamos aqui para evitar importação circular
    from app.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')
    
    from app.tasks import tasks_bp
    app.register_blueprint(tasks_bp, url_prefix='/tasks')

    # Rota de teste simples
    @app.route('/hello')
    def hello():
        return "API do Gerenciador de Tarefas funcionando!"

    return app

# Importamos os modelos no final para evitar problemas de importação
from app import models
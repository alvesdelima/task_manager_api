from app import db, bcrypt
from datetime import datetime

# Modelos são representações em Python das tabelas do nosso BD

class User(db.Model):
    """
    Modelo do Usuário. Armazena username e hash da senha.
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # Relacionamento: Um usuário pode ter várias tarefas
    # 'tasks' é o nome do atributo para acessar as tarefas do usuário
    # 'back_populates' conecta com o atributo 'owner' na classe Task
    # 'lazy=True' significa que o SQLAlchemy só carregará as tarefas quando acessarmos
    tasks = db.relationship('Task', back_populates='owner', lazy=True, cascade="all, delete-orphan")

    def __init__(self, username, password):
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Verifica se a senha fornecida bate com o hash armazenado."""
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Task(db.Model):
    """
    Modelo da Tarefa.
    """
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Chave Estrangeira: Liga a tarefa ao seu dono (Usuário)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relacionamento: Define como acessar o usuário dono desta tarefa
    owner = db.relationship('User', back_populates='tasks')

    def __repr__(self):
        return f'<Task {self.title}>'
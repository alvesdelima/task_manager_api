import os

# Pega o diretório base do projeto
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações base do aplicativo."""
    
    # Chave secreta para segurança (CSRF, sessões, etc.)
    # Em produção, isso DEVE ser uma variável de ambiente complexa!
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'voce-nunca-vai-adivinhar'
    
    # Configuração do Banco de Dados
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Chave secreta para os Tokens JWT
    # Troque isso por uma string aleatória e segura!
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'meu-jwt-super-secreto'
from app import create_app

# Cria a instância do app usando a fábrica
app = create_app()

if __name__ == '__main__':
    # debug=True reinicia o servidor automaticamente
    # NUNCA use debug=True em produção!
    app.run(debug=True)
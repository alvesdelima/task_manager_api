from flask import Blueprint, request, jsonify
from app.models import Task, User
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import logging

# Cria o Blueprint das tarefas
tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('', methods=['POST'])
@jwt_required()
def create_task():
    """
    Endpoint para criar uma nova tarefa.
    A rota é protegida, exigindo um token JWT.
    """
    try:
        # Pega o ID do usuário que está dentro do token JWT
        current_user_id = int(get_jwt_identity())
        
        data = request.get_json()
        title = data.get('title')
        description = data.get('description')

        if not title:
            return jsonify({"error": "O título é obrigatório"}), 400

        # Cria a nova tarefa, associando-a ao usuário logado
        new_task = Task(
            title=title,
            description=description,
            user_id=current_user_id
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify({
            "message": "Tarefa criada com sucesso!",
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
                "created_at": new_task.created_at
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao criar tarefa: {e}")
        return jsonify({"error": "Erro interno ao criar tarefa"}), 500

@tasks_bp.route('', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Endpoint para listar todas as tarefas DO USUÁRIO logado.
    """
    try:
        # Pega o ID do usuário do token
        current_user_id = int(get_jwt_identity())
        
        # Filtra as tarefas para pegar apenas as do usuário logado
        tasks = Task.query.filter_by(user_id=current_user_id).all()
        
        # Formata a saída
        output = []
        for task in tasks:
            output.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            })

        return jsonify({"tasks": output}), 200

    except Exception as e:
        logging.error(f"Erro ao buscar tarefas: {e}")
        return jsonify({"error": "Erro interno ao buscar tarefas"}), 500

@tasks_bp.route('/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Endpoint para marcar uma tarefa como concluída (ou reabrir).
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Busca a tarefa específica
        task = Task.query.get(task_id)

        # Verifica se a tarefa existe
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404

        # !! IMPORTANTE !!
        # Verifica se a tarefa pertence ao usuário que está logado
        if task.user_id != current_user_id:
            return jsonify({"error": "Acesso não autorizado"}), 403 # 403 = Forbidden

        # Pega o novo status (se enviado), senão, inverte o atual
        data = request.get_json()
        completed = data.get('completed')

        if completed is None:
            # Se 'completed' não foi enviado, apenas invertemos
            task.completed = not task.completed
        else:
            task.completed = bool(completed)

        db.session.commit()

        return jsonify({
            "message": "Tarefa atualizada com sucesso!",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao atualizar tarefa: {e}")
        return jsonify({"error": "Erro interno ao atualizar tarefa"}), 500


@tasks_bp.route('/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Endpoint para deletar uma tarefa específica.
    """
    try:
        current_user_id = int(get_jwt_identity())
        
        # Busca a tarefa específica
        task = Task.query.get(task_id)

        # Verifica se a tarefa existe
        if not task:
            return jsonify({"error": "Tarefa não encontrada"}), 404

        # !! IMPORTANTE !!
        # Verifica se a tarefa pertence ao usuário que está logado
        if task.user_id != current_user_id:
            return jsonify({"error": "Acesso não autorizado"}), 403 # 403 = Forbidden

        # Deleta a tarefa do banco de dados
        db.session.delete(task)
        db.session.commit()

        # Retorna uma resposta de sucesso (204 No Content é comum para DELETE)
        return '', 204

    except Exception as e:
        db.session.rollback()
        logging.error(f"Erro ao deletar tarefa: {e}")
        return jsonify({"error": "Erro interno ao deletar tarefa"}), 500
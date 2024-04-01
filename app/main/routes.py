from app.main import bp
from flask import request,jsonify
import validators
from app.models.users import Todo
from app.status_codes import HTTP_400_BAD_REQUEST,HTTP_409_CONFLICT,HTTP_500_INTERNAL_SERVER_ERROR,HTTP_201_CREATED,HTTP_401_UNAUTHORIZED,HTTP_200_OK,HTTP_404_NOT_FOUND
from app.extensions import db,bcrypt
from flask_jwt_extended import jwt_required, get_jwt,current_user



@bp.route('/')
def index():
    return 'This is The Main Blueprint'


#These routes for the todos
@bp.route('/todo', methods=['GET'])
@jwt_required()
def get_all_todos():
    try:
        # Retrieve todos associated with the current user
        todos = current_user.todos

        # Create a list to store todo data
        output = []

        # Iterate through todos and append their data to the output list
        for todo in todos:
            todo_data = {}
            todo_data['id'] = todo.id
            todo_data['title'] = todo.title
            todo_data['description'] = todo.description
            todo_data['complete'] = todo.complete
            output.append(todo_data)

        # Return the output list as a JSON response
        return jsonify(output),HTTP_200_OK

    except Exception as e:
        # Handle any exceptions that may occur
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), HTTP_500_INTERNAL_SERVER_ERROR

# #fetching respective todo

# @bp.route('/todo/<todo_id>', methods=['GET'])
# @jwt_required()
# def get_one_todo(todo_id):
#     todo = Todo.query.first()

#     if not todo:
#         return jsonify({'Message': 'You have not created any todo!'})

#     todo_data = {}
#     todo_data['id'] = todo.id
#     todo_data['title'] = todo.title
#     todo_data['description']=todo.description
#     todo_data['complete'] = todo.complete

#     return jsonify({'Message': todo_data})



# #Adding Todo
# @bp.route('/todo', methods=['POST'])
# @jwt_required()
# def create_todo():
#     data = request.get_json()
#     new_todo = Todo(title=data['title'],description=data['description'], complete=False,user_id=current_user.id)
#     db.session.add(new_todo)
#     db.session.commit()

#     return jsonify({'Message': 'Task created successfully'})


# #Completion of Todo
# @bp.route('/todo/complete/<todo_id>', methods=['PUT'])
# @jwt_required()
# def complete_todo(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()

#     if not todo:
#         return jsonify({'Message': 'No task found, please add some'})

#     todo.complete = True
#     db.session.commit()
#     return jsonify({'Message': 'Task has been completed'})


# #Deleting Todo
# @bp.route('/todo/delete/<todo_id>', methods=['DELETE'])
# @jwt_required()
# def delete_todo(todo_id):
#     todo = Todo.query.filter_by(id=todo_id).first()

#     if not todo:
#         return jsonify({'Message': 'No task found'})

#     db.session.delete(todo)
#     db.session.commit()

#     return jsonify({'Message': 'Task has been deleted successfully'})  
    

# Fetching respective todo
@bp.route('/todo/<todo_id>', methods=['GET'])
@jwt_required()
def get_one_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({'Message': 'Todo not found'}), HTTP_404_NOT_FOUND

        todo_data = {
            'id': todo.id,
            'title': todo.title,
            'description': todo.description,
            'complete': todo.complete
        }
        return jsonify({'Message': todo_data})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), HTTP_500_INTERNAL_SERVER_ERROR

# Adding Todo
@bp.route('/todo', methods=['POST'])
@jwt_required()
def create_todo():
    try:
        data = request.get_json()
        new_todo = Todo(
            title=data['title'],
            description=data['description'],
            complete=False,
            user_id=current_user.id
        )
        db.session.add(new_todo)
        db.session.commit()
        return jsonify({'Message': 'Task created successfully'}), HTTP_201_CREATED

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), HTTP_500_INTERNAL_SERVER_ERROR

# Completion of Todo
@bp.route('/todo/complete/<todo_id>', methods=['PUT'])
@jwt_required()
def complete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({'Message': 'No task found, please add some'}), HTTP_404_NOT_FOUND

        todo.complete = True
        db.session.commit()
        return jsonify({'Message': 'Task has been completed'})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), HTTP_500_INTERNAL_SERVER_ERROR

# Deleting Todo
@bp.route('/todo/delete/<todo_id>', methods=['DELETE'])
@jwt_required()
def delete_todo(todo_id):
    try:
        todo = Todo.query.get(todo_id)
        if not todo:
            return jsonify({'Message': 'No task found'}), HTTP_404_NOT_FOUND

        db.session.delete(todo)
        db.session.commit()
        return jsonify({'Message': 'Task has been deleted successfully'})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        return jsonify({'error': error_message}), HTTP_500_INTERNAL_SERVER_ERROR
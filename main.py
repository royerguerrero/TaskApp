from flask import request, make_response, redirect, render_template, session, url_for, flash
import unittest
from app import create_app
from app.firestore_service import get_users, get_todos, put_todo, delete_todo, update_todo
from flask_login import login_required, current_user
from app.forms import TodoForm, DeleteTodoFrom, UpdateTodoFrom

app = create_app()


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.route('/')
def index():
    user_ip = request.remote_addr

    response = make_response(redirect('/hello'))
    session['user_ip'] = user_ip

    return response


@app.route('/hello', methods=['GET', 'POST'])
@login_required
def hello():
    user_ip = session.get('user_ip')
    # login_form = LoginForm()
    username = current_user.id
    todo_form = TodoForm()
    delete_todo_form = DeleteTodoFrom()
    update_todo_form = UpdateTodoFrom()

    ctx = {
        'user_ip':user_ip,
        'todos':get_todos(user_id=username),
        'username':username,
        'todo_form':todo_form,
        'delete_todo_form': delete_todo_form,
        'update_todo_form': update_todo_form
    }

    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)

        flash('Tu tarea se creo con éxito!')

        return redirect(url_for('hello'))

    return render_template('hello.html', **ctx)

@app.route('/todos/delete/<todo_id>', methods=['POST'])
def delete(todo_id):
    user_id = current_user.id
    delete_todo(user_id=user_id, todo_id=todo_id)
    
    return redirect(url_for('hello'))

@app.route('/todos/update/<todo_id>/<int:done>', methods=['POST'])
def update(todo_id, done):
    user_id = current_user.id
    update_todo(user_id, todo_id, done)

    return redirect(url_for(hello))



@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('500.html', error=error)

from flask import render_template, flash, request, redirect, url_for, session
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm
from app.auth import auth
from app.firestore_service import get_user, user_put
from app.models import UserModel, UserData

@auth.route('/login', methods=['GET', 'POST'])
def login():

    login_form = LoginForm()
    ctx = {'login_form':login_form}
    
    if request.method == 'POST' and login_form.validate():
        username = login_form.username.data
        password = login_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()['password']

            if check_password_hash(password_from_db, password):
                user_data = UserData(username, password)
                user = UserModel(user_data)

                login_user(user)

                flash('Bienvenido de nuevo')
                return redirect(url_for('hello'))
            else:
                flash('La información no coincide')

        else:
            flash('El usuario no existe')

    
    return render_template('login.html', **ctx)


@auth.route('singup', methods=['GET', 'POST'])
def singup():
    singup_form = LoginForm()

    ctx = {'singup_form':singup_form}

    if singup_form.validate_on_submit():
        username = singup_form.username.data
        password = singup_form.password.data

        user_doc = get_user(username)

        if user_doc.to_dict() is None:
            password_hash = generate_password_hash(password)
            user_data = UserData(username, password_hash)
            user_put(user_data)

            user = UserModel(user_data)

            login_user(user)

            flash('Bienvenido')

            return redirect(url_for('hello'))

        else:
            flash('El usuario ya existe!')

    return render_template('singup.html', **ctx)


@auth.route('logout')
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')

    return redirect(url_for('auth.login'))

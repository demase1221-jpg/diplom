from flask import Blueprint, render_template, request, redirect
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def register():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # 🔒 Проверки
        if len(username) < 3:
            error = "Логин должен быть минимум 3 символа"
        elif len(password) < 8:
            error = "Пароль должен быть минимум 8 символов"
        elif User.query.filter_by(username=username).first():
            error = "Пользователь уже существует"
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(password)
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect('/login')

    return render_template('register.html', error=error)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    error = None

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user:
            error = "Пользователь не найден"
        elif not check_password_hash(user.password, password):
            error = "Неверный пароль"
        else:
            login_user(user)
            return redirect('/')

    return render_template('login.html', error=error)


@auth.route('/logout')
def logout():
    logout_user()
    return redirect('/login')
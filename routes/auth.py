#routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from utils.db import db
from utils.auth import login_manager  # Importa login_manager

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():    #obtenemos los datos desde el formulario
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()  #buscamos si el usuario se encuentra en la tabla
        if user and user.check_password(password):   #chequeamos que el usuario y contraseña sea correcto y le damos acceso
            login_user(user)
            return redirect(url_for('products.home'))
        else:
            flash('Usuario o Contraseña errónea, Por favor intente nuevamente', 'danger') #Caso contrario no le permite el acceso al usuario
    return render_template('login.html')



@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST': #tomamos los datos del html
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first() #chequeamos que el nombre no este registrado
        if user:
            flash('El nombre de usuario ya existe.', 'danger')
        else: #si el nombre no esta registrado aceptamos sus credenciales y lo agregamos a la Database
            new_user = User(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Usuario registrado exitosamente.', 'success')
            return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth.route('/logout')
@login_required
def logout(): #Cerramos la sesion del usuario y redirigimos al inicio
    print(f'Logging out user: {current_user.username}')
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

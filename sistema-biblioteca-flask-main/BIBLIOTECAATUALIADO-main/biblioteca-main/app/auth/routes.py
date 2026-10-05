from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app.models.user import get_user_by_username, check_user_password, create_user, listar_livros

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = get_user_by_username(username)
        
        if user and check_user_password(user, password):
            session['user_id'] = user['id'] if hasattr(user, '__getitem__') else user.id
            return redirect(url_for('auth.welcome'))
        
        flash('Usuário ou senha inválidos!', 'danger')
    
    try:
        return render_template('login.html')
    except Exception:
        return render_template('auth/login.html')

@auth_bp.route('/welcome')
def welcome():
    livros_cadastrados = listar_livros()
    try:
        return render_template('welcome.html', livros=livros_cadastrados)
    except Exception:
        return render_template('auth/welcome.html', livros=livros_cadastrados)

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))
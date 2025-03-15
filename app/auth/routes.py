from flask import render_template, request, redirect, url_for, flash, session
from . import auth
from ..utils.api import login_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        success, token, error = login_user(username, password)
        
        if success:
            session['token'] = token
            return redirect(url_for('dashboard.index'))
        else:
            flash(error or 'Invalid credentials', 'danger')
    
    return render_template('auth/login.html')

@auth.route('/logout')
def logout():
    session.pop('token', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login'))
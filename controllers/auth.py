from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db
from models.models import User, Admin
from flask_login import login_user, logout_user
from datetime import datetime
from sqlalchemy.exc import IntegrityError  

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Try logging in as Admin
        admin = Admin.query.filter_by(username=username).first()
        if admin and admin.password == password:
            login_user(admin)
            return redirect(url_for('admin.dashboard'))  # Correct route name
        
        # Try logging in as a User
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('home'))  # Correct route name
        
        flash('Invalid username or password', 'error')
        return redirect(url_for('auth.login'))  # Stay on login page if failed
    
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('auth.login'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        full_name = request.form['full_name']
        qualification = request.form['qualification']
        dob_str = request.form['dob']
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()

        admin_user = Admin.query.filter_by(username=username).first()
        if admin_user:
            flash('This username is reserved for admin. Choose another.', 'error')
            return redirect(url_for('auth.register'))
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already taken. Please choose a different one.', 'error')
            return redirect(url_for('auth.register'))  # Fix redirect

        new_user = User(
            username=username,
            password=password,
            full_name=full_name,
            qualification=qualification,
            dob=dob
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('Registration successful! Please log in.', 'success')
            print("✅ Registration Successful - Redirecting to Login")

            return redirect(url_for('auth.login'))
        except IntegrityError:
            db.session.rollback()
            flash('An error occurred. Please try again.', 'error')
    
    return render_template('register.html')

from flask import Flask, render_template
from flask_migrate import Migrate
from models import db
from controllers.auth import auth_bp
from controllers.admin import admin_bp
from sqlalchemy import inspect
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz_mastesr.db'
app.secret_key = 'qwerty'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"

from models.models import User, Admin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))  

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/tables')
def list_tables():
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return ', '.join(tables)

@app.route('/quizzes')
def quizzes():
    return render_template('quizzes.html')

@app.route('/quizzes/create')
def create_quiz():
    return render_template('create_quiz.html')

@app.route('/quizzes/<int:quiz_id>')
def attempt_quiz(quiz_id):
    return render_template('attempt_quiz.html', quiz_id=quiz_id)

def create_admin():
    with app.app_context():
        db.create_all()
        existing_admin = Admin.query.filter_by(id=1).first()
        if not existing_admin:
            admin = Admin(id=1, username="achyuth", password="1234")
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin user created.")
        else:
            print("✅ Admin user already exists.")


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True, port=5000)

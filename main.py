import markupsafe
from flask import Flask, url_for, request, render_template
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from jinja2 import Markup
from werkzeug.utils import redirect
from forms.category import CategoryForm
from forms.task import TaskForm
from datetime import datetime
import markdown

from data import db_session
from data.categories import Category
from data.tasks import Task
from data.users import User
from datetime import timedelta

db_session.global_init("db/db.db")
db_sess = db_session.create_session()
app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=365)


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/')
@app.route('/index')
def index():
    with open("README.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return render_template('index.html', html=markupsafe.Markup(html))

@app.route('/help')
def help():
    with open("README.md", "r", encoding="utf-8") as input_file:
        text = input_file.read()
    html = markdown.markdown(text)
    return render_template('doc.html', html=markupsafe.Markup(html))

@app.route('/logout')
def logout():
    logout_user()
    return render_template('index.html', message="Вы успешно вышли из системы")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == request.form.get('login')).first()
        # user.set_password('password')
        # print(user.hashed_password)
        if user:
            if user.check_password(request.form.get('password')):
                login_user(user)

                return render_template('base.html', message="Вы успешно вошли в систему", login=user.name)
            else:
                return render_template('base.html', message="Неправильный пароль")
        else:
            return render_template('base.html', message="Неправильный логин")
    return render_template('base.html', message="Непредвиденная ошибка")


@app.route('/categories')
def categories():
    form = CategoryForm()
    db_sess = db_session.create_session()
    categories = db_sess.query(Category).all()
    return render_template('categories.html', categories=categories, form=form)

@app.route('/createcategory', methods=['POST'])
def createcategory():
    form = CategoryForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        category = Category(
            title=form.title.data,
        )
        db_sess.add(category)
        db_sess.commit()
        print('Категория создана')
    return redirect('/categories')

@app.route('/deletecategory/<int:id>')
def deletecategory(id):
    db_sess = db_session.create_session()
    category = db_sess.query(Category).filter(Category.id == id).first()
    db_sess.delete(category)
    db_sess.commit()
    print('Категория удалена')
    return redirect('/categories')

@app.route('/tasks/<int:catid>')
def tasks():
    form = TaskForm()
    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).all()
    return render_template('categories.html', categories=categories, form=form)

@app.route('/tasksall')
def tasksall():

    db_sess = db_session.create_session()
    tasks = db_sess.query(Task).all()
    categories = db_sess.query(Category).all()
    form = TaskForm(categories=categories)

    return render_template('tasks.html', tasks=tasks, form=form)

@app.route('/createtask', methods=['POST'])
def createtask():
    form = TaskForm()
    # if form.validate_on_submit():
    db_sess = db_session.create_session()
    task = Task(
        title=form.title.data,
        deadline=form.deadline.data,
        category_id=form.category.data,
        created_date=datetime.now(),
        done=0
    )
    # task = Task(
    #     title='wrwerwer',
    #     deadline=datetime.now(),
    #     category_id=1,
    #     created_date=datetime.now(),
    #     done=0
    # )

    db_sess.add(task)
    db_sess.commit()
    print('Задача создана')
    return redirect('/tasksall')

@app.route('/deletetask/<int:id>')
def deletetask(id):
    db_sess = db_session.create_session()
    task = db_sess.query(Task).filter(Task.id == id).first()
    db_sess.delete(task)
    db_sess.commit()
    print('Задача удалена')
    return redirect('/tasksall')

app.run(port=8080, host='127.0.0.1')
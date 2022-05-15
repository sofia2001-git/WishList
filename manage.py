from app import create_app
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, request, abort
from app.database import db
from app.forms.login import LoginForm
from app.forms.register_user import RegisterForm
from app.users.user import User
from app.wishes.wish import Wish
from add_function import add_user

app = create_app()
login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    message = ''
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        message = "Неправильный логин или пароль"
    return render_template('login.html', title='Авторизация', form=form, message=message)


@app.route("/admin")
@login_manager.user_loader
def admin():
    users = db.session.query(User).all()
    wishes = db.session.query(Wish).all()
    return render_template("show_info.html", users=users)


@app.route('/admin/register_user', methods=['GET', 'POST'])
@login_required
def register_user():
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db.session.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        add_user(form.surname.data, form.name.data, form.age.data, form.nick.data,
                 form.email.data, form.password.data)
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@app.route('/admin/edit_user/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_users(id):
    form = RegisterForm()
    if request.method == "GET":
        user = db.session.query(User).filter(User.id == current_user or User.id == 1).first()
        if user:
            form.surname.data = user.surname
            form.name.data = user.name
            form.age = user.age
            form.nick = user.nick
            form.email = user.email

        else:
            abort(404)
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.id == current_user or User.id == 1).first()
        if user:
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.nick = form.nick.data
            user.email = form.email.data
            db.session.commit()
            return redirect('/admin')
        else:
            abort(404)
    return render_template('edit_user.html', title='Редактирование пользователя', form=form)


@app.route('/admin/delete_user/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_user(id):
    user = db.session.query(User).filter(User.id == current_user or User.id == 1).first()
    if user:
        db.session.delete(user)
        db.session.commit()
    else:
        abort(404)
    return redirect('/admin')


if __name__ == '__main__':
    app.run()
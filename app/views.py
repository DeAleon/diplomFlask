from config import app
from flask import render_template, request, redirect, url_for, flash, make_response, session
from flask_login import login_required, login_user, current_user, logout_user
from models import Game, User, db
from forms import UserForm, LoginForm, GameForm
from slugify import slugify




@app.route('/')
def menu():
    title = 'Главная страница'
    game = 'Игры'
    reg = 'Регистарция'
    cart = 'Корзина'
    log = 'Вход'
    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'log': log,
        'cart': cart,
    }
    return render_template('menu.html', **template_context)


@app.route('/login/', methods=['post', 'get'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('menu'))
    form = LoginForm()
    title = 'Главная страница'
    game = 'Игры'
    reg = 'Регистарция'
    cart = 'Корзина'
    log = 'Вход'
    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'form': form,
        'log': log,
        'cart': cart,
    }
    if form.validate_on_submit():
        user = db.session.query(User).filter(User.username == form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('cart_'))
        flash("Неверный логин или пароль", 'error')
        return redirect(url_for('login'))
    return render_template('login.html', **template_context)


@app.route('/game/')
def game():
    title = 'Главная страница'
    game = 'Игры'
    games = Game.query.all()
    reg = 'Регистарция'
    cart = 'Корзина'
    log = 'Вход'
    len_game = len(games)
    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'log': log,
        'cart': cart,
        'games': games,
        'len_game': len_game
    }
    return render_template('game.html', **template_context)


@app.route('/registration/', methods=['GET', 'POST'])
def registration():
    form = UserForm()
    title = 'Главная страница'
    game = 'Игры'
    reg = 'Регистарция'
    cart = 'Корзина'
    log = 'Вход'
    if form.validate_on_submit():
        name = form.name.data
        login = form.login.data
        email = form.email.data
        password = form.password.data
        age = form.age.data

        users = User(name=name, email=email, username=login, slug=slugify(login), age=age)
        users.set_password(password)
        db.session.add(users)
        db.session.commit()

        flash("Регистрация прошла успешно", "success")
        return redirect(url_for('menu'))
    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'form': form,
        'cart': cart,
        'log': log,
    }

    return render_template('user.html', **template_context)

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    flash("Вы успешно вышли из акаунта.")
    return redirect(url_for('login'))

@app.route('/cart/')
@login_required
def cart_():
    title = 'Главная страница'
    game = 'Игры'
    reg = 'Регистарция'
    log = 'Вход'
    cart = 'Корзина'
    cart_error = 'Извините но ваша карзина пустая!'

    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'log': log,
        'cart': cart,
        'cart_error': cart_error,
    }
    return render_template('cart.html', **template_context)

@app.route('/game/add_game/', methods=['GET', 'POST'])
def add_game():
    form = GameForm()
    title = 'Главная страница'
    game = 'Игры'
    reg = 'Регистарция'
    cart = 'Корзина'
    log = 'Вход'
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        cost = form.cost.data
        size = form.size.data
        age_limited = form.age_limited.data

        games = Game(title=title, description=description, cost=cost,
                     size=size, age_limited=age_limited, slug=slugify(title))
        db.session.add(games)
        db.session.commit()

        #flash("Message Received", "success")
        return redirect(url_for('add_game'))
    template_context = {
        'title': title,
        'game': game,
        'reg': reg,
        'form': form,
        'cart': cart,
        'log': log,
    }

    return render_template('add_game.html', **template_context)

if __name__ == '__main__':
    app.run(debug=True)


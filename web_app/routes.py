from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from .models import Quote, User, UserQuote
from .helpers import is_valid_email, is_strong_password, add_quote_to_user
from . import db
import random

routes = Blueprint('routes', __name__)


@routes.route("/")
def home():
    username = session.get('username')
    if not username:
        return redirect(url_for('routes.login'))
    return render_template("index.html", username=username)


# API endpoint to get a random quote
@routes.route('/api/quote/random', methods=['GET'])
def get_random_quote():
    max_id = db.session.query(db.func.max(Quote.id)).scalar()
    if max_id is not None:
        random_id = random.randint(1, max_id)
        quote = Quote.query.get(random_id)
        if quote:
            username = session.get('username')
            if username:
                user = User.query.filter_by(username=username).first()
                if user:
                    add_quote_to_user(user, quote)
            return jsonify({
                'quote_text': quote.quote_text,
                'quote_author': quote.quote_author
            })
    return jsonify({'message': 'No quotes found'}), 404


# API endpoint to search quotes by author
@routes.route('/api/quote/search', methods=['GET'])
def search_quotes_by_author():
    author_name = request.args.get('author')
    if not author_name:
        return jsonify({'error': 'Author name parameter is required'}), 400

    quote = Quote.query.filter_by(quote_author=author_name).first()
    if quote:
        username = session.get('username')
        if username:
            user = User.query.filter_by(username=username).first()
            if user:
                add_quote_to_user(user, quote)
        result = [{
            'quote_text': quote.quote_text,
            'quote_author': quote.quote_author
        }]
        return jsonify(result)
    return jsonify({'message': 'No quotes found for author'}), 404


@routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not is_valid_email(email):
            error_message = "Invalid email format"
            return render_template("registration.html", error_message=error_message)

        if not is_strong_password(password):
            error_message = 'Password must be at least 8 characters long, contain both letters and numbers'
            return render_template("registration.html", error_message=error_message)

        if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
            error_message = "User Already Exists"
            return render_template("registration.html", error_message=error_message)

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username
        return redirect("/")
    return render_template("registration.html")


@routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        data = request.form
        username = data.get('username')
        password = data.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            error_message = 'Invalid username or password'
            return render_template("login.html", error_message=error_message)
        session['username'] = username
        return redirect("/")
    return render_template("login.html")


@routes.route('/profile')
def profile():
    username = session.get('username')
    if not username:
        return redirect('/login')

    user = User.query.filter_by(username=username).first()
    if not user:
        return redirect('/login')

    quotes = UserQuote.query.filter_by(user_id=user.id).all()
    total_quotes_received = sum([quote.no_of_times_received for quote in quotes])

    quotes_data = []
    for user_quote in quotes:
        quote = Quote.query.get(user_quote.quote_id)
        quotes_data.append({
            'quote_text': quote.quote_text,
            'quote_author': quote.quote_author,
            'no_of_times_received': user_quote.no_of_times_received
        })

    return render_template("profile.html", username=username, total_quotes_received=total_quotes_received,
                           quotes_data=quotes_data)


@routes.route('/logout')
def logout():
    session.clear()
    return redirect('/')

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quotes.db'  # SQLite database
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = '565656787890'
    db.init_app(app)

    with app.app_context():
        from .routes import routes
        from .models import Quote
        from .quotes_data import quotes_data
        db.create_all()

        for quote_info in quotes_data:
            quote_text = quote_info['quote_text']
            quote_author = quote_info['quote_author']

            # Check if the quote already exists in the database
            existing_quote = Quote.query.filter_by(quote_text=quote_text, quote_author=quote_author).first()

            if not existing_quote:
                # If quote does not exist, add it to the database
                quote = Quote(quote_text=quote_text, quote_author=quote_author)
                db.session.add(quote)

        db.session.commit()  # Commit all quotes to the database

        app.register_blueprint(routes, url_prefix="/")

    return app
import re
from . import db
from .models import UserQuote


# Helper functions for validation
def is_valid_email(email):
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)


def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"[a-zA-Z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    return True


# Function to add a quote to UserQuote table
def add_quote_to_user(user, quote):
    user_quote = UserQuote.query.filter_by(user_id=user.id, quote_id=quote.id).first()
    if user_quote:
        user_quote.no_of_times_received += 1
    else:
        new_user_quote = UserQuote(user_id=user.id, quote_id=quote.id)
        db.session.add(new_user_quote)
    db.session.commit()

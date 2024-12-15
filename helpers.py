from flask import redirect, render_template, session
from functools import wraps
import re


def error(message):
    return render_template("error.html", message=message)


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def shorten_url(long_url):
    # Define the regular expression pattern
    pattern = re.compile(r'(?:https?://)?([a-zA-Z0-9.-]+)')

    # Match the pattern in the long link
    match = pattern.match(long_url)

    # Extract the base home page link
    base_home_page = match.group(1) if match else None
    return base_home_page




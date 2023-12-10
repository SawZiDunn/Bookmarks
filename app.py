from flask import Flask, request, session, flash, render_template, redirect
from cs50 import SQL
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import error, login_required, shorten_url
from datetime import datetime
import pytz

app = Flask(__name__)

app.jinja_env.filters["shorten_url"] = shorten_url

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///bookmarks.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    bookmarks: list = db.execute(
        "SELECT name, url, id, folder_id, time FROM bookmarks WHERE user_id=? ORDER BY time DESC",
        session["user_id"])

    for dic in bookmarks:
        dic["folder_name"] = db.execute("SELECT name FROM folders WHERE id=? and user_id=?", dic["folder_id"], session["user_id"])[0]["name"]
        del dic['folder_id']

    if request.form.get("specific"):
        bookmarks = [bookmark for bookmark in bookmarks if bookmark["folder_name"] == request.form.get("specific")]

    return render_template("index.html", bookmarks=bookmarks)


@app.route("/folders")
@login_required
def folder_index():
    folders: list = db.execute("SELECT name, id, time FROM folders WHERE user_id=? AND name!=?", session["user_id"],
                               "None")

    return render_template("folders.html", folders=folders)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return error("Please provide Username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return error("Please provide Password")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid Username and/or Password")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == 'POST':
        username = request.form.get('username')
        # can I do that?
        # usernames = db.execute('SELECT username FROM users')

        if not username:
            return error("Please provide username!")

        password = request.form.get('password')
        confirmation = request.form.get('confirmation')

        if not password or not confirmation:
            return error('Please enter and confirm your password!')
        elif password != confirmation:
            return error("Please confirm your password!")

        rows = db.execute('SELECT * FROM users WHERE username=?', username)
        if len(rows) != 0:
            return error('Username already exists!')

        db.execute('INSERT INTO users (username, hash) VALUES (?, ?)',
                   username, generate_password_hash(password))
        return redirect('/')

    else:
        return render_template('register.html')


@app.route("/add_bookmark", methods=["GET", "POST"])
@login_required
def add_bookmark():
    current_time = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        name = request.form.get("name")
        url = request.form.get("url")
        folder = request.form.get("folder")

        if folder == "new_folder":
            folder = request.form.get("new_folder")
            db.execute("INSERT INTO folders (name, user_id, time) VALUES (?, ?, ?)", folder, session["user_id"],
                       current_time)

        folder_id = db.execute("SELECT id FROM folders WHERE name=? AND user_id=?", folder, session["user_id"])

        if not folder_id:  # if the None folder does not exit
            db.execute("INSERT INTO folders (name, user_id, time) VALUES (?, ?, ?)", folder, session["user_id"], current_time)
            folder_id = db.execute("SELECT id FROM folders WHERE name=? AND user_id=?", folder, session["user_id"])

        folder_id = folder_id[0]["id"]

        db.execute("INSERT INTO bookmarks (name, url, folder_id, user_id, time) VALUES (?, ?, ?, ?, ?)", name, url,
                   folder_id, session["user_id"], current_time)
        flash("New Bookmark Added!")
        return redirect("/")

    else:
        folders = db.execute("SELECT name FROM folders WHERE user_id=? and name != ?", session["user_id"], "None")
        return render_template("add_bookmark.html", folders=folders)


@app.route("/add_folder", methods=["POST"])
@login_required
def add_folder():
    current_time = datetime.now(pytz.timezone("US/Eastern")).strftime("%Y-%m-%d %H:%M:%S")
    if request.method == "POST":
        new_folder_name = request.form.get("folder_name")
        db.execute("INSERT INTO folders (name, user_id, time) VALUES (?, ?, ?)", new_folder_name, session["user_id"],
                   current_time)
        flash("New Folder Added!")
    return redirect("/folders")


@app.route("/edit", methods=["POST"])
@login_required
def edit():
    file_type = request.form.get("type")
    if file_type == "bookmark":
        name = request.form.get("bookmark_name")
        url = request.form.get("url")

        db.execute("UPDATE bookmarks SET name=?, url=? WHERE id=? AND user_id=?", name, url,
                   request.form.get("bookmark_id"), session["user_id"])
        flash("Bookmark Edited!")
        return redirect("/")
    else:
        name = request.form.get("folder_name")
        db.execute("UPDATE folders SET name=? WHERE id=? AND user_id=?", name,
                   request.form.get("folder_id"), session["user_id"])
        flash("Folder Name Edited!")
        return redirect("/folders")


@app.route("/delete", methods=["POST"])
@login_required
def delete():
    file_type = request.form.get("delete")
    if file_type == "bookmark":
        db.execute("DELETE from bookmarks WHERE id=? AND user_id=?", request.form.get("Bid_to_delete"),
                   session["user_id"])
        flash("Bookmark Deleted!")
        return redirect("/")

    else:
        db.execute("DELETE from bookmarks WHERE folder_id=? AND user_id=?", request.form.get("Fid_to_delete"),
                   session["user_id"])
        db.execute("DELETE from folders WHERE id=? AND user_id=?", request.form.get("Fid_to_delete"),
                   session["user_id"])

        flash("Folder Deleted!")
        return redirect("/folders")


if __name__ == '__main__':
    app.run(debug=True)

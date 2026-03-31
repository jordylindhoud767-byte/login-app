from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

# User model (this is a table in the database)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# Login page
@app.route("/")
def login_page():
    return render_template("login.html", error=None)

# Check login
@app.route("/login", methods=["POST"])
def check_login():
    username = request.form["username"]
    password = request.form["password"]

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return render_template("welcome.html", username=username)
    else:
        return render_template("login.html", error="Incorrect username or password")

# Register page
@app.route("/register")
def register_page():
    return render_template("register.html", error=None)

# Save new user
@app.route("/register", methods=["POST"])
def register_user():
    username = request.form["username"]
    password = request.form["password"]

    # Check if username already exists
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return render_template("register.html", error="Username already exists")

    # Save new user to database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("login_page"))

if __name__ == "__main__":
    app.run(debug=True)
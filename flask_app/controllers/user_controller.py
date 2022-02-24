from flask_app import app
from flask import render_template,request,redirect,session,flash
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register/user", methods=["POST"])
def register():
    if not User.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)

    data = {
        "first_name" :request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/dashboard")
def welcome_user():
    if session['login'] == False:
        return redirect("/")

    data = {
        "id":session['user_id']
    }
    user = User.one_user(data)
    recipes = Recipe.get_all_recipes(data)
    print(recipes)
    return render_template('dashboard.html',user=user, recipes = recipes)

@app.route("/login", methods=["POST"])
def login():
    # see if the username provided exists in the database
    data = { "email" : request.form["email2"] }
    user_in_db = User.get_by_email(data)
    print(user_in_db)
    # user is not registered in the db
    if not user_in_db:
        flash("Invalid Email", "login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password2']):
        # if we get False after checking the password
        flash("Invalid Password", "login")
        return redirect('/')
    # if the passwords matched, we set the user_id into session
    session['user_id'] = user_in_db.id
    session['login'] = True
    # never render on a post!!!
    return redirect("/dashboard")

@app.route("/logout")
def logout():
    session.pop("user_id")
    session['login'] = False
    return redirect("/")

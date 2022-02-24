from flask_app import app
from flask import render_template,request,redirect,session
from flask_app.models.recipe import Recipe
from flask_app.models.user import User


@app.route("/create_recipe", methods = ["POST"])
def create_recipe():
    return redirect("/recipes/new")

@app.route("/recipes/new")
def recipes_new():
    if session['login'] == False:
        return redirect("/")    
    return render_template("recipes.html")

@app.route("/save_recipe", methods=["POST"])
def new_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    data = {
        "name" :request.form["recipe_name"],
        "description" : request.form["description"],
        "instruction" : request.form["instruction"],
        "under_thirty" : request.form["under_thirty"],
        "user_id" : session["user_id"],
        "date_made" : request.form["date_made"],

    }
    recipe_id = Recipe.save_recipe(data)
    # session["user_id"] = user_id
    return redirect("/dashboard")

@app.route("/recipes/<int:recipe_id>")
def recipe_info(recipe_id):
    if session['login'] == False:
        return redirect("/")
    data = {
        "id" : recipe_id
    }
    recipe = Recipe.one_recipe(data)
    data2 = {
        "id":session['user_id']
    }
    user = User.one_user(data2)
    return render_template("recipe_info.html",recipe = recipe, user= user)

@app.route("/edit/recipes/<int:recipe_id>")
def edit_recipe(recipe_id):
    if session['login'] == False:
        return redirect("/")
    data = {
        "id" : recipe_id
    }
    # session['recipe_id'] = recipe_id
    recipe = Recipe.one_recipe(data)
    print(recipe)
    return render_template("edit_recipe.html",recipe = recipe)

@app.route("/update_recipe", methods = ["POST"])
def update_recipe():
    if not Recipe.validate_recipe(request.form):
        return redirect(f"/edit/recipes/{request.form['recipe_id']}")
    data = {
        "id": request.form["recipe_id"],
        "name": request.form["recipe_name"],
        "description": request.form["description"],
        "instruction" : request.form["instruction"],
        "date_made" : request.form["date_made"],
        "under_thirty" : request.form["under_thirty"]
    }
    Recipe.update(data)
    return redirect("/dashboard")

@app.route('/delete/<int:recipe_id>')
def delete_user(recipe_id):
    data = {
        "id":recipe_id
    }
    Recipe.delete(data)
    return redirect('/dashboard')
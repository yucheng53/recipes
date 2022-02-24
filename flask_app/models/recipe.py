from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app

class Recipe():
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]        
        self.instruction = data["instruction"]
        self.under_thirty = data["under_thirty"]
        self.date_made = data["date_made"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instruction, under_thirty, user_id, date_made, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instruction)s, %(under_thirty)s, %(user_id)s, %(date_made)s, NOW(), NOW() )"
        return connectToMySQL('recipes_schema').query_db( query, data )

    @classmethod
    def get_all_recipes(cls,data):
        query = "SELECT * FROM recipes WHERE user_id = %(id)s;"
        results = connectToMySQL('recipes_schema').query_db(query,data)
        recipes = []
        for recipe in results:
            recipes.append( cls(recipe) )
        print(recipes)
        return recipes

    @classmethod
    def one_recipe(cls,data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL("recipes_schema").query_db(query, data)
        return cls(results[0])

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, date_made=%(date_made)s, under_thirty=%(under_thirty)s, updated_at = NOW() WHERE id=%(id)s; "
        return connectToMySQL('recipes_schema').query_db( query, data )
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM recipes WHERE id=%(id)s; "
        return connectToMySQL('recipes_schema').query_db( query, data )

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe["recipe_name"]) < 3:
            flash("Name must be at least 3 characters.", "error")
            is_valid = False
        if len(recipe["description"]) < 3:
            flash("Description must be at least 3 characters.", "error")
            is_valid = False
        if len(recipe["instruction"]) < 3:
            flash("Instruction must be at least 3 characters.", "error")
            is_valid = False
        if not recipe["date_made"]:
            flash("All fields must be filled out.", "error")
            is_valid = False
        if "under_thirty" not in recipe:
            flash("All fields must be filled out.", "error")
            is_valid = False
        return is_valid
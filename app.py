from flask import Flask, render_template, request,session
import dbcontext

app = Flask(__name__)

app.secret_key = "nskex23xdr"

def get_all_recipes():
    """fetch all available recipes for user"""
    db_answer = None
    con = dbcontext.dbConnection("recipes.db")

    db_answer = con.execute_read_query(f"""
                                        select 
                                        recipes.recipes_name, ingredients.ingredient_name
                                        from recipes_ingredients 
                                        join recipes 
                                        on recipes.id = recipes_id 
                                        join ingredients on 
                                        ingredients.id = ingredient_id;""")
    all_recipes = [recipes for recipes in db_answer]
    recipe_dict={}
    for recipe in all_recipes:
        if recipe[0] not in recipe_dict:
            recipe_dict[recipe[0]]=[recipe[1]]
        else:
            recipe_dict[recipe[0]].append(recipe[1])
    return recipe_dict

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/recipes",methods=["POST",'GET'])
def recipes():
    ''''''
    #resignation of alphaValues check - need upgrade
    ingredients = request.form.getlist("name")
    ingredients = ",".join(["'" + str(elem) + "'" for elem in ingredients])
    db_answer = None
    con = dbcontext.dbConnection("recipes.db")
    db_answer = con.execute_read_query(f"""
                                        select 
                                        recipes.recipes_name,count(recipes.recipes_name) as ingredients_count 
                                        from recipes_ingredients 
                                        join 
                                        recipes 
                                        on recipes.id = recipes_id 
                                        join ingredients 
                                        on ingredients.id = ingredient_id 
                                        where ingredients.ingredient_name in ({ingredients}) 
                                        group by recipes.recipes_name;""")
    recipes_list = [recipes[0] for recipes in db_answer if recipes[1] >= 3]

    if ingredients:
        return render_template("recipes.html",recipes_list=recipes_list)
    return render_template("recipes.html",ingredients=ingredients)


@app.route("/add_recipies",methods=['GET'])
def add_recipies():

    return render_template("add_recipies.html")


@app.route("/added_to_cookbook",methods=["POST",'GET'])
def added_to_cookbook():
    recipe = cook_recipe()
    recipe.add_recipe_ingredient(recipe.add_Ingredients(),recipe.add_recipe())
    return render_template("added_to_cookbook.html",name= session.get('recipe_name'))
class cook_recipe():
    def __init__(self):
        self.con = dbcontext.dbConnection("recipes.db")
        self.ingredients = request.form.getlist("name")
    def add_Ingredients(self):
        db_answer = None
        ingredients_str = ",".join(["'" + str(elem) + "'" for elem in self.ingredients])
        db_answer = self.con.execute_read_query(f"""
                                               select ingredient_name 
                                               from ingredients 
                                               where ingredient_name in ({ingredients_str});""")
        print(list(db_answer))
        newIngredients = [ing for ing in self.ingredients if ing not in [db[0] for db in db_answer]]

        new_ingredients_str = ",".join(["('" + str(elem) + "')" for elem in newIngredients])
        if newIngredients:
            create_users = f"""INSERT INTO ingredients (ingredient_name)
                                VALUES {new_ingredients_str};"""
            self.con.execute_query(create_users)
        return self.con.execute_read_query(f"""
                                           select id 
                                           from ingredients 
                                           where ingredient_name in ({ingredients_str});""")

    def add_recipe(self):
        db_answer = self.con.execute_read_query(f"""
                                               select id 
                                               from recipes 
                                               where 
                                               recipes_name in ('{session.get('recipe_name')}');""")
        if not db_answer:
            create_users = f"""INSERT INTO recipes (recipes_name) VALUES ('{session.get('recipe_name')}');"""
            self.con.execute_query(create_users)
        return self.con.execute_read_query(f"""select id from recipes where recipes_name in ('{session.get('recipe_name')}');""")

    def add_recipe_ingredient(self,ing_list,recipe_list):
        ing_rec_str = ",".join(["('" + str(recipe_list[0][0]) + "','" + str(ing[0]) + "')" for ing in ing_list])
        create_users = f"""
                            INSERT INTO 
                            recipes_ingredients (recipes_id,ingredient_id) 
                            VALUES {ing_rec_str};"""
        self.con.execute_query(create_users)

@app.route("/add_recipies_ingr",methods=['GET'])
def add_recipies_ingr():
    ingr_amt = int(request.args.get('ingr_amount'))
    
    add_recipe_name = request.args.get('name')
    session['recipe_name'] = add_recipe_name
    return render_template("add_recipies_ingr.html",ingr_amt=ingr_amt,name=add_recipe_name)


@app.route("/show_all_recipes")
def show_all_recipes():
    recipe_dict = get_all_recipes()
    return render_template("show_all_recipes.html",recipe_dict=recipe_dict)

@app.route("/delete_recipe_form",methods = ['GET'])
def delete_recipe_form():
    """gets name of deleted object and removes it from database"""
    db_connection = dbcontext.dbConnection("recipes.db")
    to_delete = [i for i in request.args.keys()]
    get_id_statement= f"""
                    select id from recipes where recipes_name = '{to_delete[0]}'"""
    recipe_id = db_connection.execute_read_query(get_id_statement)
    delete_statement_recipes=f"""
                     DELETE FROM recipes where recipes_name = '{to_delete[0]}'   
                    """
    delete_statement_recipes_ingredients = f"""
                     DELETE FROM recipes_ingredients where recipes_id = {recipe_id[0][0]}
                    """
    
    db_connection.execute_query(delete_statement_recipes)
    db_connection.execute_query(delete_statement_recipes_ingredients)

    return show_all_recipes()

@app.route("/modify_recipes",methods = ['GET'])
def modify_recipes():
    recipe_dict = get_all_recipes()
    return render_template("modify_recipes.html",recipe_dict=recipe_dict)


def alpha_values(user_ingredients):
        user_input = [skladnik.strip().lower() for skladnik in user_ingredients]
        if all(skladnik.replace(' ','').isalpha() for skladnik in user_input):
            return user_input
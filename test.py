import dbcontext
import json
import dbcontext


db_answer = None
con = dbcontext.dbConnection("recipes.db")

db_answer = con.execute_read_query_json(f"""
                                    select 
                                    recipes.recipes_name, ingredients.ingredient_name
                                    from recipes_ingredients 
                                    join recipes 
                                    on recipes.id = recipes_id 
                                    join ingredients on 
                                    ingredients.id = ingredient_id;""")
# all_recipes = [recipes for recipes in db_answer]
# recipe_dict={}
# for recipe in all_recipes:
#     if recipe[0] not in recipe_dict:
#         recipe_dict[recipe[0]]=[recipe[1]]
#     else:
#         recipe_dict[recipe[0]].append(recipe[1])


json_output = json.dumps(db_answer)
print(db_answer)
print(json_output)

recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter the Recipe Name: ")
    cooking_time =int(input("Enter the cooking time (in minutes): "))
    ingredients = input("Enter ingredients separated by commas: ").split(',')
    ingredients = [ingredient.strip() for ingredient in ingredients]

    recipe = {
        'name': name,
        'cooking_time': cooking_time,
        'ingredients': ingredients
    }
    
    return recipe
    

num_recipes = int(input("How many recipes would you like to enter?: "))

for num in range(num_recipes):
    recipe = take_recipe()

    for ingredient in recipe['ingredients']:
        if ingredient not in ingredients_list:
            ingredients_list.append(ingredient)
    recipes_list.append(recipe)

for recipe in recipes_list:
    cooking_time = recipe['cooking_time']
    num_ingredients = len(recipe['ingredients'])

    if cooking_time < 10 and num_ingredients < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and num_ingredients >=4:
        difficulty = "Medium"
    elif cooking_time >= 10 and num_ingredients < 4:
        difficulty = "Intermediate"
    else:
        difficulty = "Hard"
    
    recipe['difficulty'] = difficulty

    #instead of concatinating strings I used and f-string for simplicity
    # \n means new line
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

print("\nAll Ingredients used:")
for ingredient in sorted(ingredients_list):
    print(ingredient)
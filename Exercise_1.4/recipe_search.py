import pickle

def display_recipe(recipe):
    # Using an f string again instead of concatination
    print(f"\nRecipe: {recipe['name']}")
    print(f"Cooking Time: {recipe['cooking_time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")

def search_ingredient(data):
    all_ingredients = data["all_ingredients"]

    if not all_ingredients:
        print("No ingredients found")
        return
    print("\nAvailable Ingredients")
    for index, ingredient in enumerate(all_ingredients):
        print(f"{index}. {ingredient}")
    try:
        choice = int(input("\nEnter the number for the ingredient you would like to search: "))
        ingredient_searched = all_ingredients[choice]
    except (ValueError):
        print("Invalid input. Please enter a valid number from the list")
    except (IndexError):
        print("Invalid input. Please enter a valid number from the list")
    else:
        print(f"\nRecipes with {ingredient_searched}")
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["ingredients"]:
                display_recipe(recipe)
            else:
                print("No recipes found with this ingredient")

filename = input("Enter the filename with your recipe data: ")
try:
    with open(filename, "rb") as file:
        data = pickle.load(file)
except FileNotFoundError:
    print("File not found. Please check the filename and try again")
else:
    search_ingredient(data)
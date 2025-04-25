# Importing packages

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import sessionmaker


# Creating engine objoect
engine = create_engine('mysql://cf-python:Branic2!@localhost/task_database')

# Storing base
Base = declarative_base()

# Create session
Session = sessionmaker(bind=engine)
session = Session()

# Recipe Model


class Recipe(Base):
    __tablename__ = 'final_recipes'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe ID: {self.id} - Name: {self.name} - Difficulty: {self.difficulty}>"

    def __str__(self):
        return (
            f"{'-'*5}\n"
            f"Recipe: {self.name}\n"
            f"Cooking Time: {self.cooking_time} Minutes\n"
            f"Ingredients: {self.ingredients}\n"
            f"Difficulty: {self.difficulty}\n"
            f"{'-'*5}\n"
        )
    
    # Calculate the difficulty
    def calculate_difficulty(self):
        ingredient_list = self.ingredients.split(', ')
        num_ingredients = len(ingredient_list)
        if self.cooking_time < 10:
            if num_ingredients < 4:
                self.difficulty = 'Easy'
            else:
                self.difficulty = 'Medium'
        else:
            if num_ingredients < 4:
                self.difficulty = 'Intermediate'
            else:
                self.difficulty = 'Hard'
    
    # Returning the ingredients
    def return_ingredients_as_list(self):
        return self.ingredients.split(', ') if self.ingredients else []


Base.metadata.create_all(engine)


# Part 3: Creating the recipe


def create_recipe():
    while True:
        name = input("Enter recipe name: ")
        if len(name) > 50:
            print("Error: Name cannot be longer than 50 characters.")
        elif not name.isalpha():
            print("Error: Name can only contain letters.")
        else:
            break

    while True:
        cooking_time = input("Enter cooking time in minutes: ")
        if not cooking_time.isnumeric():
            print("Error: Cooking time must be a number.")
        else:
            cooking_time = int(cooking_time)
            break

# Collecting ingredients
    ingredients = []
    n = int(input("Enter the number of ingredients: "))

    for i in range(n):
        ingredient = input(f"Enter ingredient {i + 1}: ")
        ingredients.append(ingredient)

    ingredients_str = ', '.join(ingredients)

    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )

    recipe_entry.calculate_difficulty()

    session.add(recipe_entry)
    session.commit()

    print("Recipe added successfully.\n")

# Function 2 viewing all recipes


def view_all_recipes():
    recipes = session.query(Recipe).all()
    if not recipes:
        print("No recipes found.\n")
    else:
        for recipe in recipes:
            print(recipe)

# Function 3 searching for a recipe


def search_by_ingredient():

    recipes_count = session.query(Recipe).count()
    if recipes_count == 0:
        print("No recipes found.\n")
        return None
    results = session.query(Recipe).all()
    all_ingredients = []
    for result in results:
        ingredients_list = result.ingredients.split(', ')
    for ingredient in ingredients_list:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)
    
    print("\nAvailable ingredients:")
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i + 1}. {ingredient}")
    selected_ingredient = input("Select an ingredient by number: ")

    try:
        selected_index = [int(i) for i in selected_ingredient.split()]
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    if any(i < 1 or i > len(all_ingredients) for i in selected_index):
        print("Invalid choice. Please select a valid ingredient number.")
        return None
    
    search_ingredients = [all_ingredients[i - 1] for i in selected_index]
    conditions = []

    for ingredient in search_ingredients:
        like_ingredient = f'%{ingredient}%'
        conditions.append(Recipe.ingredients.like(like_ingredient))

    from sqlalchemy import and_
    matching_recipes = session.query(Recipe).filter(and_(*conditions)).all()
    if not matching_recipes:
        print("No recipes found with that ingredient.\n")
    else:
        for recipe in matching_recipes:
            print(recipe)


def edit_recipe():
    # Check for table entries
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return

    # Retrieve and display all recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - Name: {recipe.name}")

    # Prompt user to select recipe by ID
    try:
        selected_id = int(input("Enter the ID of the recipe you'd like to update: "))
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    recipe_ids = [r.id for r in recipes]
    if selected_id not in recipe_ids:
        print("Error: Invalid recipe ID. Try again.")
        return

    # Fetch the selected recipe
    recipe = session.query(Recipe).filter_by(id=selected_id).one()

    # Show current recipe details
    print("\nCurrent recipe details:")
    print(f"1. Name: {recipe.name}")
    print(f"2. Ingredients: {recipe.ingredients}")
    print(f"3. Cooking Time: {recipe.cooking_time} minutes")

    # Ask user which field to update
    field_choice = input("Enter the number of the field you'd like to update (1, 2, or 3): ")

    if field_choice == "1":
        new_name = input("Enter the new name: ").strip()
        if not new_name.isalpha() or len(new_name) > 50:
            print("Error: Name must contain only letters and be no longer than 50 characters.")
            return
        recipe.name = new_name

    elif field_choice == "2":
        try:
            num_ingredients = int(input("How many ingredients does the recipe have? "))
        except ValueError:
            print("Error: Please enter a valid number.")
            return

        new_ingredients = []
        for i in range(num_ingredients):
            ingredient = input(f"Enter ingredient {i+1}: ").strip()
            new_ingredients.append(ingredient)
        
        recipe.ingredients = ", ".join(new_ingredients)

    elif field_choice == "3":
        new_time = input("Enter the new cooking time (in minutes): ").strip()
        if not new_time.isdigit():
            print("Error: Cooking time must be a number.")
            return
        recipe.cooking_time = int(new_time)

    else:
        print("Invalid choice. Please select 1, 2, or 3.")
        return

    # Recalculate difficulty and commit changes
    recipe.difficulty = recipe.calculate_difficulty()
    session.commit()
    print("Recipe updated successfully!")


def delete_recipe():
    # Check if there are any recipes
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return

    # Fetch and display available recipes
    recipes = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:")
    for recipe in recipes:
        print(f"ID: {recipe.id} - Name: {recipe.name}")

    # Prompt for recipe ID to delete
    try:
        selected_id = int(input("Enter the ID of the recipe you'd like to delete: ").strip())
    except ValueError:
        print("Error: Please enter a valid numeric ID.")
        return

    # Check if ID exists
    valid_ids = [r.id for r in recipes]
    if selected_id not in valid_ids:
        print("Error: Invalid recipe ID. Please select from the list.")
        return

    # Retrieve recipe by ID
    recipe = session.query(Recipe).filter_by(id=selected_id).one()

    # Confirm deletion
    confirmation = input(f"Are you sure you want to delete '{recipe.name}'? Type 'yes' to confirm: ").strip().lower()

    if confirmation == "yes":
        session.delete(recipe)
        session.commit()
        print(f"Recipe '{recipe.name}' has been deleted.")
    else:
        print("Deletion canceled.")


def main_menu():
    menu_options = {
        '1': ("Create a recipe", create_recipe),
        '2': ("View all recipes", view_all_recipes),
        '3': ("Search by ingredient", search_by_ingredient),
        '4': ("Update a recipe", edit_recipe),
        '5': ("Delete a recipe", delete_recipe),
    }

    while True:
        print("\nWelcome! What would you like to do? Type the number of your choice:")
        for key, (description, _) in menu_options.items():
            print(f"{key}. {description}")
        print("Type 'quit' to exit the program.")

        user_choice = input("Your choice: ").strip().lower()

        if user_choice == 'quit':
            print("See you next time!")
            break
        elif user_choice in menu_options:
            _, action = menu_options[user_choice]
            action()
        else:
            print("Invalid choice! Please enter 1–5 or 'quit'.")

    # Close session and engine after exiting
    session.close()
    engine.dispose()

# Start the menu


main_menu()

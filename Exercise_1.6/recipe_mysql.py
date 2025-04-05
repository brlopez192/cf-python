import mysql.connector


def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        return "Intermediate"
    else:
        return "Hard"


def create_recipe(conn, cursor):
    name = input("Enter recipe name: ")
    ingredients_input = input("Enter ingredients (comma separated): ")
    ingredients = [item.strip() for item in ingredients_input.split(',')]
    cooking_time = int(input("Enter cooking time in minutes: "))

    # Calculate difficulty using the function
    difficulty = calculate_difficulty(cooking_time, ingredients)

    # Join ingredients for storage
    ingredients_str = ", ".join(ingredients)

    cursor.execute("""
        INSERT INTO Recipes (name, ingredients, cooking_time, difficulty)
        VALUES (%s, %s, %s, %s)
    """, (name, ingredients_str, cooking_time, difficulty))

    conn.commit()
    print("Recipe added successfully.\n")


    conn.commit()
    print("Recipe added successfully.\n")

# Search for a recipe
def search_recipe(conn, cursor):
    search_term = input("Enter an ingredient to search for: ").strip().lower()

    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    found = False
    for recipe in results:
        ingredients_list = [i.strip().lower() for i in recipe[2].split(',')]
        if search_term in ingredients_list:
            print(recipe)
            found = True

    if not found:
        print("No recipes found with that ingredient.\n")

# Update a recipe
def update_recipe(conn, cursor):
    recipe_id = input("Enter the ID of the recipe to update: ")
    print("What would you like to update?")
    print("1. Name\n2. Ingredients\n3. Cooking Time")
    choice = input("Enter your choice (1-3): ")

    if choice == "1":
        new_name = input("Enter new name: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_name, recipe_id))
    elif choice == "2":
        new_ingredients = input("Enter new ingredients (comma separated): ")
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (new_ingredients, recipe_id))
    elif choice == "3":
        new_time = int(input("Enter new cooking time (minutes): "))
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_time, recipe_id))
    else:
        print("Invalid choice.")
        return

    conn.commit()
    print("Recipe updated successfully.\n")

# Delete a recipe
def delete_recipe(conn, cursor):
    recipe_id = input("Enter the ID of the recipe to delete: ")
    cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
    conn.commit()
    print("Recipe deleted successfully.\n")


# Main Menu
def main_menu(conn, cursor):
    while True:
        print("\n--- Recipe Manager ---")
        print("1. Create a new recipe")
        print("2. Search recipe by ingredient")
        print("3. Update a recipe")
        print("4. Delete a recipe")
        print("Type 'quit' to exit")

        while True:
            choice = input("Enter a choice (1-4) or type 'quit' to exit: ").strip().lower()

            if choice == "1":
                create_recipe(conn, cursor)
            elif choice == "2":
                search_recipe(conn, cursor)
            elif choice == "3":
                update_recipe(conn, cursor)
            elif choice == "4":
                delete_recipe(conn, cursor)
            elif choice == "quit":
                print("Exiting... Goodbye!")
                break
            else:
                print("Invalid input, please try again.")



if __name__ == "__main__":
    conn = mysql.connector.connect(
        host='localhost',
        user='cf-python',
        password='Branic2!'
    )

    cursor = conn.cursor()

    # Ensure DB and table exist
    cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
    cursor.execute("USE task_database")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50),
        ingredients VARCHAR(255),
        cooking_time INT,
        difficulty VARCHAR(20)
    )
    """)

    # Start the menu
    main_menu(conn, cursor)

    # Commit and close connection when done
    conn.commit()
    cursor.close()
    conn.close()
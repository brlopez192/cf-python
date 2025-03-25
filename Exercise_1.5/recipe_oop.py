class Recipe:
    all_ingredients = set()

    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time
        self.calculate_difficulty()
    
    def get_cooking_time(self):
        return self.cooking_time
    
    def add_ingredients(self, *args):
        self.ingredients.extend(args)
        self.update_all_ingredients()
        self.calculate_difficulty()
    
    def get_ingredients(self):
        return self.ingredients
    
    def calculate_difficulty(self):
        if self.cooking_time < 10:
            if len(self.ingredients) < 4:
                self.difficulty = "Easy"
            else:
                self.difficulty = "Medium"
        else:
            if len(self.ingredients) < 4:
                self.difficulty = "Intermediate"
            else:
                self.difficulty = "Hard"
    
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
    
    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients
    
    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)
    
    def __str__(self):
        ingredient_list = ""
        for ingredient in self.ingredients:
            ingredient_list += ingredient + ", "
        ingredient_list = ingredient_list.rstrip(", ")
        
        return (f"Recipe: {self.name}\nIngredients: {ingredient_list}\n"
                f"Cooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n")
    
    def recipe_search(self, data, search_term):
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)

# Creating recipe objects
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
print(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

# Searching for recipes containing specific ingredients
print("Recipes containing 'Water':")
tea.recipe_search(recipes_list, "Water")

print("Recipes containing 'Sugar':")
tea.recipe_search(recipes_list, "Sugar")

print("Recipes containing 'Bananas':")
tea.recipe_search(recipes_list, "Bananas")
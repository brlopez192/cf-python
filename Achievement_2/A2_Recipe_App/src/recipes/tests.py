from django.test import TestCase
from .models import Recipe
# Create your tests here.


class RecipeModelTest(TestCase):
    def setUpTestData():
        # Set up non-modified objects used by all test methods
        Recipe.objects.create(name='Soup',
                              ingredients='water, salt, pepper, chicken, noodles',
                              cooking_time=30,
                              difficulty='easy'
                              )
      
    def test_recipe_name(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the "name" field and use it to query its data
        field_label = recipe._meta.get_field('name').verbose_name

        # Compare the vale to the result
        self.assertEqual(field_label, 'name')

    def test_recipe_ingredients(self):
        # Get a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Get the metadata for the "ingredients" field and use it to query its data
        field_label = recipe._meta.get_field('ingredients').verbose_name

        # Compare the vale to the result
        self.assertEqual(field_label, 'ingredients')

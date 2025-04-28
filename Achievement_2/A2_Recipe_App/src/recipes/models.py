from django.db import models

# Create your models here.

difficulity_choices = (
    ('easy', 'Easy'),
    ('intermediate', 'Intermediate'),
    ('hard', 'Hard')
)


class Recipe(models.Model):
    name = models.CharField(max_length=120)
    ingredients = models.TextField(default='No ingredients')
    cooking_time = models.IntegerField()
    difficulty = models.CharField(
        max_length=12,
        choices=difficulity_choices,
        default='easy'
    )

    def __str__(self):
        return str(self.name)


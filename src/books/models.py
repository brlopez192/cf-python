from django.db import models
from django.shortcuts import reverse

# Create your models here.

genre_choices = (('classic', 'Classic'),
                 ('romance', 'Romance'),
                 ('comic', 'Comic'),
                 ('fantasy', 'Fantasy'),
                 ('horror', 'Horror'),
                 ('education', 'Education')
                 )
book_type_choices = (('hardcover', 'Hardcover'),
                     ('ebook', 'Ebook'),
                     ('audiobook', 'Audiobook')
                     )


class Book(models.Model):
    name = models.CharField(max_length=120)
    author_name = models.CharField(max_length=120)
    price = models.FloatField(help_text='in US dollars $')
    genre = models.CharField(max_length=120,
                             choices=genre_choices,
                             default='classic')
    book_type = models.CharField(max_length=120, 
                                 choices=book_type_choices, 
                                 default='hardcover')
    pic = models.ImageField(upload_to='books', default='no_picture.jpg')

    def __str__(self):
        return str(self.name)
 
    def get_absolute_url(self):
        return reverse('books:detail', kwargs={'pk': self.pk})
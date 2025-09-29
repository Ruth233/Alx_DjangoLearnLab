from django.db import models

# Create your models here.
class Author(models.Model):
    """
    Represents a book author.
    - name: The author's full name.
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Represents a book written by an Author.
    - title: Book title.
    - publication_year: Year published.
    - author: ForeignKey to Author (one Author -> many Books).
    """
    title = models.CharField(max_length=200)
    publication_year = models.PositiveIntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"

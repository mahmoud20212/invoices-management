from django.db import models
from django.core.validators import MinValueValidator

class Store(models.Model):
    logo = models.ImageField(upload_to='logos/')
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True)
    tax_number = models.IntegerField(validators=[MinValueValidator(0)])
    address = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = [
            "-created_at",
        ]


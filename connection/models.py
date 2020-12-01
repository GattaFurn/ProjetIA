from django.db import models

COLOR_CHOICES = [
    ('BL', 'Blue'),
    ('PK', 'Pink'),
    ('YW', 'Yellow'),
    ('GN', 'Green'),
    ('VT', 'Violet'),
    ('RD', 'Red'),
    ('OE', 'Orange'),
    ('CN', 'Cyan'),
]
# Create your models here.
class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    color = models.CharField(max_length=2,choices = COLOR_CHOICES,default = 'BL')

    def __str__(self):
        return str(self.id) +" - "+ self.pseudo
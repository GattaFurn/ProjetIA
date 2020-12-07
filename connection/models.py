from django.db import models

COLOR_CHOICES = [
    ('BL', '#0099ff'),
    ('PK', '#ff99ff'),
    ('YW', '#ffcc66'),
    ('GN', '#80ff80'),
    ('VT', '#bf80ff'),
    ('RD', '#b30000'),
    ('OE', '#ff8c1a'),
    ('CN', '#80ffff'),
]
# Create your models here.
class Utilisateur(models.Model):
    pseudo = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    color = models.CharField(max_length=2,choices = COLOR_CHOICES,default = 'BL')

    def __str__(self):
        return str(self.id) +" - "+ self.pseudo
from django.db import models

# Create your models here.

class Project(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        # Shows name, start and end time for admin
        return self.name

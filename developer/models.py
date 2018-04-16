from django.db import models


class Message(models.Model):
    #user = models.ForeignKey(User, on_delete=models.CASCADE)
    #project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    created_on = models.DateField(auto_now_add=True)
    message = models.TextField(null=True)
    
    def __str__(self):
        return self.name + ", " + self.phone + ", " + self.email + ", " + self.message

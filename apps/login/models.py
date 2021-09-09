from django.db import models


# Create your models here.
class User(models.Model):
    loginEmail = models.CharField(max_length=50, primary_key=True)
    dateCreated = models.DateTimeField()
    password = models.CharField(max_length=45)

    #linkedToContactId = models.OneToOneField('Contact', on_delete=models.CASCADE)

    def __str__(self):
        return self.loginEmail


from django.db import models

# Create your models here.
class Users(models.Model):
    user = models.CharField(max_length=500, unique=True)
    login_password = models.CharField(max_length=600)

# Relación Many to One. Many sería el password, porque tiene la foreignkey. Y one sería el user.
class Password(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    desc = models.CharField(max_length=500)
    pwd = models.CharField(max_length=600)




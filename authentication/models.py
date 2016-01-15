from django.db import models


class User(models.Model):
    email = models.CharField(primary_key=True, max_length=30)
    name_surname = models.CharField(max_length=50)
    password = models.CharField(max_length=40)


class Application(models.Model):
    id = models.IntegerField(primary_key=True)


class Instance(models.Model):
    user = models.ForeignKey(User, related_name='instances')
    app = models.ForeignKey(Application, related_name='instances')
    time = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=30)

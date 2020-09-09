from djongo import models
from django import forms


class User(models.Model):
    _id = models.ObjectIdField()
    user_id = models.CharField(max_length=100)
    user_pw = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    major = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class Circle(models.Model):
    _id = models.ObjectIdField()
    name = models.CharField(max_length=100)
    leader = models.EmbeddedField(model_container=User)
    member = models.ArrayField(model_container=User)

    def __str__(self):
        return self.name

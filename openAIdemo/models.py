from django.db import models


class Summoner(models.Model):
    name = models.CharField(max_length=100)


#  from openAIdemo.models import Summoner
# smer = Summoner(name="J.K. Rowling")
# smer.save()
# smers = Summoner.objects.all()
# print(smers)

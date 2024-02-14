from django.db import models

# Create your models here.
class Candidate(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(null=False,max_length=20)
    name = models.CharField(max_length=20)
    test_attempted = models.IntegerField(default=0)
    points = models.FloatField(default=0.0)

class Questions(models.Model):
    qid = models.BigAutoField(primary_key=True, auto_created=True)
    que = models.TextField()
    a = models.CharField(max_length=255)
    b = models.CharField(max_length=255)
    c = models.CharField(max_length=255)
    d = models.CharField(max_length=255)
    ans = models.CharField(max_length=20)

class Result(models.Model):
    resultid = models.BigAutoField(primary_key=True, auto_created=True)
    username = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    time = models.TimeField(auto_now=True)
    attempt = models.IntegerField()
    right = models.IntegerField()
    wrong = models.IntegerField()
    points = models.FloatField(default=0)

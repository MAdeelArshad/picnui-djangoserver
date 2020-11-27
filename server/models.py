from djongo import models

# Create your models here.


class Routine(models.Model):
    name = models.CharField(max_length=255, unique=True)

class RobotProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Points(models.Model):
    points = models.JSONField()
    robotProfile = models.ForeignKey(RobotProfile, on_delete=models.CASCADE)










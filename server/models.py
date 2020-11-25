from djongo import models

# Create your models here.


class Routine(models.Model):
    name = models.CharField(max_length=255, unique=True)



class RobotProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    points = models.JSONField(default={})
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)




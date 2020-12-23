from djongo import models

# Create your models here.

class RobotProfile(models.Model):
    name = models.CharField(max_length=255, unique=True)
    linkedRoutine = models.IntegerField()

class Routine(models.Model):
    name = models.CharField(max_length=255, unique=True)



class Points(models.Model):
    points = models.JSONField()
    routine = models.ForeignKey(Routine, on_delete=models.CASCADE)










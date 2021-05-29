from django.db import models

class Event(models.Model):
    ID = models.AutoField(primary_key=True, auto_created=True, editable=False)
    NAME = models.CharField(max_length=100)
    LONG = models.FloatField(default=0.0)
    LAT = models.FloatField(default=0.0)

    def __str__(self):
        return str(self.ID)
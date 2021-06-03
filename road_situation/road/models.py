from django.db import models
from numpy.lib.function_base import blackman

class Event(models.Model):
    type_choices = [
        (0, 'Binh thuong'),
        (1, 'Cay nga'),
        (2, 'Hoa hoan'),
        (3, 'Ngap lut'),
        (4, 'Duong xau'),
        (5, 'Ket xe'),
        (6, 'Rac thai'),
        (7, 'Tai nan giao thong')
    ]
    ID = models.AutoField(primary_key=True, auto_created=True, editable=False)
    LABEL = models.IntegerField(choices=type_choices, default=1)
    LONG = models.FloatField(default=0.0)
    LAT = models.FloatField(default=0.0)
    TIME = models.DateTimeField(auto_now_add=True, blank=True)
    IMAGE = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.ID)
from django.db import models

# Create your models here.
class BatteryType(models.Model):
    name = models.CharField(max_length=16)
    def __str__(self):
        return self.name

class Battery(models.Model):
    type = models.ForeignKey(BatteryType, on_delete=models.PROTECT)
    def __str__(self):
        return self.type.name

class Trait(models.Model):
    name = models.CharField(max_length=32)
    cost = models.ManyToManyField(Battery)
    def __str__(self):
        return self.name

class Card(models.Model):
    name = models.CharField(max_length=64)
    def __str__(self):
        return self.name

class Construct(Card):
    attack = models.IntegerField()
    defense = models.IntegerField()
    traits = models.ManyToManyField(Trait)

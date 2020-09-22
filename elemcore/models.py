from django.db import models
import itertools
import math

# Create your models here.
class BatteryType(models.Model):
    name = models.CharField(max_length=16)
    icon = models.URLField(max_length=512)
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
    picture = models.URLField(max_length=255)
    def __str__(self):
        return self.name

    @property
    def cost(self):
        cost_list = []
        if self.construct:
            cost_list.append(self.construct.attack)
            cost_list.append(self.construct.defense)

            trait_costs = []
            for trait in self.construct.traits.all():
                cost_list.append([x.type.name for x in trait.cost.all()])

        def parse_cost_list(cost_list):
            named = []
            total = 0
            for x in cost_list:
                try:
                    x = int(x)
                    total += x
                except TypeError:
                    [named.append(each) for each in x ]

            result = [math.ceil(total/2)] + named
            print(total/2)
            print("result:", result)
            #print(len(result))
            return(result)
        return parse_cost_list(cost_list)


class Construct(Card):
    type = 'CONSTRUCT'
    attack = models.IntegerField()
    defense = models.IntegerField()
    traits = models.ManyToManyField(Trait, blank=True)

from django.db import models
import itertools
import math

def cost_to_html(base_cost, batteries=[]):
    print("to_html got:", base_cost, batteries)
    # Takes = [base cost (int), [battery objects]]
    icons=[]
    for battery in batteries:
        icons.append('<img src="{}" height="16px" width="16px">'.format(battery.type.icon))
    if base_cost == 0:
        base_cost = ''

    result = str(base_cost)+ ''.join(icons)
    print("to_html output:", result)
    return result

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
    long_desc = models.TextField(max_length=4096)
    def __str__(self):
        return self.name

class Ability(models.Model):
    cost = models.ManyToManyField(Battery)
    text = models.CharField(max_length=512)
    def __str__(self):
        return self.text

    @property
    def get_cost(self):
        return 0, self.cost.all()



    @property
    def cost_as_html(self):
        base_cost, batteries = self.get_cost
        return cost_to_html(base_cost, batteries)



class Card(models.Model):
    name = models.CharField(max_length=64)
    picture = models.URLField(max_length=256)
    flavor_text = models.TextField(max_length=256)

    def __str__(self):
        return self.name

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        if self.construct:
            for trait in self.construct.traits.all():
                for battery in trait.cost.all():
                    batteries.append(battery)
            base_cost = math.ceil((self.construct.attack + self.construct.defense) /2)
        #result = base_cost, batteries]
        return base_cost, batteries

    @property
    def nameless_cost(self):
        return self.cost[0]

    @property
    def named_cost(self):
        return self.cost[1]

    @property
    def converted_cost(self):
        return nameless_cost + len(named_cost)

    @property
    def cost_as_html(self):
        base_cost, batteries = self.get_cost
        return cost_to_html(base_cost, batteries)

class Construct(Card):
    attack = models.IntegerField()
    defense = models.IntegerField()
    traits = models.ManyToManyField(Trait, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)

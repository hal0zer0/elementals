from django.db import models
import itertools
import math

def cost_to_html(cost_list):
    print("Converting cost to html")
    nameless = ''
    named_as_icons = []
    for item in cost_list:
        try:
            nameless = int(item)
        except TypeError:
            named = item
            next
        named_as_icons.append('<img src="{}" height="16" width="16px">'.format(named.type.icon))

    print("List of images:", named_as_icons)
    result = str(nameless) + " " + ''.join(named_as_icons)
    print(result)
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
    def cost_as_html(self):
        return cost_to_html(self.cost.all())


class Card(models.Model):
    name = models.CharField(max_length=64)
    picture = models.URLField(max_length=256)
    flavor_text = models.TextField(max_length=256)

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

            # Where we actually apply the math
            result = [math.ceil(total/2)] + named
            return(result)
        return parse_cost_list(cost_list)

    @property
    def nameless_cost(self):
        return self.cost[0]

    @property
    def named_cost(self):
        return self.cost[1:]

    @property
    def converted_cost(self):
        return nameless_cost + len(named_cost)

class Construct(Card):
    attack = models.IntegerField()
    defense = models.IntegerField()
    traits = models.ManyToManyField(Trait, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)

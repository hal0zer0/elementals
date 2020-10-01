from django.db import models
from django.contrib.auth.models import User
import itertools
import math


def cost_to_html(base_cost, batteries=[]):
    print("to_html got:", base_cost, batteries)
    # Takes = [base cost (int), [battery objects]]
    icons = []
    for battery in batteries:
        icons.append('<img src="{}" height="16px" width="16px">'.format(battery.type.icon))

    if base_cost == 0:
        base_cost = ''
    result = str(base_cost) + ''.join(icons)
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


class Rarity(models.Model):
    level = models.PositiveIntegerField()
    label = models.CharField(max_length=16)

    def __str__(self):
        return self.label


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


class CardSubtype(models.Model):
    name = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    name = models.CharField(max_length=64)
    picture = models.URLField(max_length=256)
    flavor_text = models.TextField(max_length=256, blank=True)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)
    subtype = models.ForeignKey(CardSubtype, on_delete=models.PROTECT, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    public = models.BooleanField(default=False)

    @property
    def card_type(self):
        if hasattr(self, 'construct'):
            return "CONSTRUCT"
        elif hasattr(self, 'action'):
            return "ACTION"
        elif hasattr(self, 'mod'):
            return "MOD"
        else:
            return "Unknown"

    def __str__(self):
        return self.name

    @property
    def cost_as_html(self):
        # Each card type has a different calculation cost because they add up their costs differently
        if hasattr(self, 'action'):
            base_cost, batteries = self.action.get_cost
        elif hasattr(self, 'construct'):
            base_cost, batteries = self.construct.get_cost
        elif hasattr(self, 'mod'):
            base_cost, batteries = self.mod.get_cost
        return cost_to_html(base_cost, batteries)

    @property
    def attack_value(self):
        if self.card_type == 'CONSTRUCT':
            return self.construct.attack
        else:
            return None

    @property
    def defense_value(self):
        if hasattr(self, 'construct'):
            return self.construct.defense
        else:
            return None


class Construct(Card):
    attack = models.PositiveIntegerField(default=1)
    defense = models.PositiveIntegerField(default=1)
    traits = models.ManyToManyField(Trait, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for trait in self.construct.traits.all():
            for battery in trait.cost.all():
                batteries.append(battery)
        base_cost = math.ceil((self.construct.attack + self.construct.defense) / 2)

        print("Output of get_cost", base_cost, batteries)
        return base_cost, batteries




class ActionEffect(models.Model):
    effect = models.TextField(max_length=4096)
    cost = models.ManyToManyField(Battery)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)

    def __str__(self):
        return self.effect


class Action(Card):
    effects = models.ManyToManyField(ActionEffect)
    card_type = "ACTION"
    def __str__(self):
        return self.name

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for effect in self.action.effects.all():
            for battery in effect.cost.all():
                batteries.append(battery)
        return base_cost, batteries


class ModEffect(models.Model):
    effect = models.TextField(max_length=4096)
    cost = models.ManyToManyField(Battery)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)

    def __str__(self):
        return self.effect


class Mod(Card):
    effects = models.ManyToManyField(ModEffect)

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for effect in self.mod.effects.all():
            for battery in effect.cost.all():
                print("Mod Battery Found")
                batteries.append(battery)
        return base_cost, batteries

class Deck(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=64)
    cards = models.ManyToManyField(Card, through='DeckPassThrough')
    public = models.BooleanField(default=False)
    image = models.URLField(max_length=256)
    def __str__(self):
        return self.name

class DeckPassThrough(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)

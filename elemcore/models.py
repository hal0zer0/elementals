from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.safestring import mark_safe
import itertools
import math


def cost_to_html(base_cost, batteries=[]):
    # Takes = [base cost (int), [battery objects]]
    icons = []
    for battery in batteries:
        icons.append('<img src="{}" height="16px" width="16px">'.format(battery.type.icon))

    if base_cost == 0:
        base_cost = ''
    result = str(base_cost) + ''.join(icons)
    return result


# Models
class BatteryType(models.Model):
    """
    The system allows for an arbitrary number of Battery types, with the initial four being Earth, Fire, Air, Water
    """
    name = models.CharField(max_length=16)
    icon = models.URLField(max_length=512)

    def __str__(self):
        return self.name


class Battery(models.Model):
    """
    A 'battery' is the equivalent of MTG's 'land/mana', however batteries are NOT part of the deck.  Each turn, a player
    may CHOOSE one new battery of any type to add to their pool.
    """
    type = models.ForeignKey(BatteryType, on_delete=models.PROTECT)

    def __str__(self):
        return self.type.name

    class Meta:
        verbose_name_plural = "Batteries"


class Trait(models.Model):
    """
    Traits are the basic (passive) characteristics of a card.  Examples in MTG would be Flying, Defender, Lifelink, etc.
    Each trait has an associated cost which is added to the cost of casting the card.  Flight, for example, may have a
    cost of 2 AIR batteries.  If that's the case, adding Flight to a construct would increase its casting cost by 2 AIR.
    """
    name = models.CharField(max_length=32)
    cost = models.ManyToManyField(Battery)
    long_desc = models.TextField(max_length=4096)

    def __str__(self):
        return self.name

    @property
    def get_cost(self):
        return 0, self.cost.all()

    @property
    def cost_as_html(self):
        base_cost, batteries = self.get_cost
        return cost_to_html(base_cost, batteries)


class Rarity(models.Model):
    """
    Rarity in Elementals works in a somewhat unique way.  More powerful/cost efficient traits are marked with a higher
    rarity, and all decks in Elementals have a specific number of cards of each rarity allowed.
    """
    level = models.PositiveIntegerField()
    label = models.CharField(max_length=16)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name_plural = "Rarities"


class Ability(models.Model):
    """
    Abilities are the ACTIVE pproperties of constructs.  An active ability does not add to the construct's casting cost,
    but activating the ability has cost.  An example ability may be something like "Tap two FIRE batteries to do one damage
    to any target"
    """
    cost = models.ManyToManyField(Battery)
    text = models.CharField(max_length=512)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Abilities"

    def __str__(self):
        return mark_safe(self.cost_as_html + self.text)

    @property
    def get_cost(self):
        return 0, self.cost.all().order_by('type')

    @property
    def cost_as_html(self):
        base_cost, batteries = self.get_cost
        return cost_to_html(base_cost, batteries)

    @property
    def cost_as_string(self):
        result = " ".join([battery.type.name for battery in self.cost.all()])
        print(result)
        return result

    @property
    def converted_cost(self):
        base_cost, batteries = self.get_cost
        return batteries.count()


class CardSubtype(models.Model):
    """
    Subtypes are simply labels intended to be used by traits and abilities.  For example, if a Construct has a subtype
    of 'cat', there may be a mod or ability that applies to Cats.
    """
    name = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self):
        return self.name


class Card(models.Model):
    """
    The base class upon which most others are built.  Cards hold 'universal' characteristics such as Name and Picture
    """
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
    """
    Constructs are equivalent to MTG's 'creatures'.  They have a base casting cost, attack/defense values, and optional
    passive traits and active abilities.
    """
    attack = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(0)])
    defense = models.PositiveIntegerField(default=1, validators=[MaxValueValidator(10), MinValueValidator(1)])
    traits = models.ManyToManyField(Trait, blank=True)
    abilities = models.ManyToManyField(Ability, blank=True)

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for trait in self.construct.traits.all():
            for battery in trait.cost.all().order_by('type'):
                batteries.append(battery)
        base_cost = math.ceil((self.construct.attack + self.construct.defense) / 2)

        return base_cost, batteries




class ActionEffect(models.Model):
    """
    It is necessary to separate the card from the card's action.  Action Effects are the spells that can be cast by
    Action cards.  This allows an effect to exist on more than one card, and a card to have more than one effect.
    """
    effect = models.TextField(max_length=4096)
    cost = models.ManyToManyField(Battery)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)

    def __str__(self):
        return self.effect


class Action(Card):
    """
    Actions are similar to MTG's Sorcery and Instant spells.  Actions take effect as they're cast and then discarded.
    """
    effects = models.ManyToManyField(ActionEffect)
    card_type = "ACTION"

    def __str__(self):
        return self.name

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for effect in self.action.effects.all():
            for battery in effect.cost.all().order_by('type'):
                batteries.append(battery)
        return base_cost, batteries


class ModEffect(models.Model):
    effect = models.TextField(max_length=4096)
    cost = models.ManyToManyField(Battery)
    rarity = models.ForeignKey(Rarity, on_delete=models.PROTECT)

    def __str__(self):
        return self.effect


class Mod(Card):
    """
    Mods are the equivalent of Enchantments in MTG.  A mod can be cast and placed on the battlefield to alter the state
    of play.  Unlike actions, they remain on the battlefield until destroyed by another card.
    """
    effects = models.ManyToManyField(ModEffect)

    @property
    def get_cost(self):
        base_cost = 0
        batteries = []
        for effect in self.mod.effects.all():
            for battery in effect.cost.all().order_by('type'):
                batteries.append(battery)
        return base_cost, batteries


class Deck(models.Model):
    """
    Decks are just a collection of cards, however this required a "pass-through" model so that multiple instances
    of a card can exist in the same deck.
    """
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

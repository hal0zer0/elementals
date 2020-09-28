from django.contrib import admin
from elemcore import models as emodels

# Register your models here.
@admin.register(emodels.Construct)
class ConstructAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Trait)
class TraitAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Battery)
class BatteryAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.BatteryType)
class BatteryTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Ability)
class AbilityAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Action)
class ActionAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.ActionEffect)
class ActionEffectAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Rarity)
class RarityAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.CardSubtype)
class CardSubtypeAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Mod)
class ModAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.ModEffect)
class ModEffectAdmin(admin.ModelAdmin):
    pass

@admin.register(emodels.Deck)
class DeckAdmin(admin.ModelAdmin):
    pass
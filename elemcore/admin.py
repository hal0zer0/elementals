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
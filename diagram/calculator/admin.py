from django.contrib import admin

from diagram.calculator.models import Food, Record, Eated


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    pass


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    pass


@admin.register(Eated)
class EatedAdmin(admin.ModelAdmin):
    pass

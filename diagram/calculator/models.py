from django.db import models
from math import ceil
from django.db.models import FloatField, CharField, ForeignKey, PROTECT, ManyToManyField, ImageField

from diagram.person.models import User, Person
from diagram.utils.model_mixins import BaseModelMixin


class Record(BaseModelMixin):
    person = ForeignKey(Person, verbose_name='Пользователь', on_delete=PROTECT, related_name='records')
    bolus = FloatField('Итог расчета', null=True, blank=True)
    sugar_value = FloatField('Уровень глюкозы в крови', null=True, blank=True)
    food_intakes = ManyToManyField('Eated', related_name='records')

    @property
    def sum_he(self):
        """Сумма хлебных едениц съеденных продуктов"""
        return sum([food_intake.he for food_intake in self.food_intakes.all()])

    @property
    def calc(self):
        # [УП/УК+ (ТСК –ЦСК)/КЧ] x ФС – АИ.
        return (((self.person.ddi_coef * self.sum_he) + self.sugar_level_on_time) / self.person.sensitivity_coeff) * 0.84

    @property
    def sugar_level_on_time(self):
        return self.sugar_value - self.person.now_coeff

    def __str__(self):
        return f'{self.DTC} - {self.person.short_name} - {self.sugar_value}'


class Eated(BaseModelMixin):
    food = ForeignKey('Food', verbose_name='Продукт', related_name='eateds', on_delete=PROTECT, null=True, blank=True)
    weight = FloatField('Вес продукта', null=True, blank=True)

    @property
    def he(self):
        """Расчет хлебных едениц на вес"""
        return round(self.food.ch * self.weight / 100 / 12, 1)

    def __str__(self):
        return f'{self.food} - {self.weight}'


class Food(BaseModelMixin):
    name = CharField('Название', max_length=30, null=True, blank=True)
    ch = FloatField('Углеводы на 100г', null=True, blank=True)
    img = ImageField(verbose_name='Изображение', null=True, blank=True)

    def __str__(self):
        return self.name

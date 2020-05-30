from django.db import models
from django.db.models import FloatField, CharField, ForeignKey, PROTECT, ManyToManyField, ImageField

from diagram.person.models import User, Person
from diagram.utils.model_mixins import BaseModelMixin


class Record(BaseModelMixin):
    person = ForeignKey(Person, verbose_name='Пользователь', on_delete=PROTECT, related_name='records')
    # bolus = FloatField('Итог расчета')
    foods = ManyToManyField('Food', related_name='records')


class Food(BaseModelMixin):
    name = CharField('Название', max_length=30, null=True, blank=True)
    ch = FloatField('Углеводы на 100г', null=True, blank=True)
    img = ImageField(verbose_name='Изображение', null=True, blank=True)

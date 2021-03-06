from datetime import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models import CharField, OneToOneField, PROTECT, BooleanField, EmailField, DateField, FloatField, \
    IntegerField
from django.utils.translation import gettext_lazy as _

from diagram.utils.model_mixins import BaseModelMixin


class CustomUserManager(UserManager):
    """
    Переписанные методы для создания пользователя без использование поля username
    """
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Эл.почта должна быть указана обязательно')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_email_verify', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser, BaseModelMixin):
    # Переназначение контекстного менеджера
    objects = CustomUserManager()
    REQUIRED_FIELDS = []  # Обязательные поля для пользователя
    USERNAME_FIELD = 'email'  # В качестве логина используется эл.почта пользователя
    email = EmailField(_('email address'), unique=True)
    is_email_verify = BooleanField('Email подтвержден', default=False)
    # Поля имя и фамилии переносятся в модель Person
    first_name = None
    last_name = None
    username = None

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')


class Person(BaseModelMixin):
    first_name = CharField('Имя', max_length=50)
    last_name = CharField('Фамилия', max_length=50, default='', blank=True)
    user = OneToOneField(User, verbose_name='Пользователь', on_delete=PROTECT, related_name='person', null=True, blank=True )

    birthday = DateField(null=True, blank=True)

    MALE = 'm'
    FEMALE = 'w'

    GENDERS = (
        (MALE, 'Мужской'),
        (FEMALE, 'Женский'),
    )
    gender = CharField(max_length=1, choices=GENDERS, null=True, blank=True)

    weight = FloatField(null=True, blank=True)
    height = IntegerField(null=True, blank=True)

    ddi = FloatField('Суточная доза инсулина', null=True, blank=True)

    @property
    def ddi_coef(self):
        """Углеводный коэффициент"""
        return 12 * self.ddi / 500

    coeff_morning = FloatField('Утренний коэффициент', null=True, blank=True)
    coeff_day = FloatField('Дневной коэффициент', null=True, blank=True)
    coeff_evening = FloatField('Вечерний коэффициент', null=True, blank=True)
    coeff_night = FloatField('Ночной коэффициент', null=True, blank=True)

    def coeff_on_hour(self, hour_now):
        """Возврат коэффициент на час в сутках"""
        times = (
            (0, 5, self.coeff_night,),
            (6, 11, self.coeff_morning,),
            (12, 17, self.coeff_day,),
            (18, 23, self.coeff_evening,),
        )
        for dt in times:
            if hour_now in range(dt[0], dt[1]+1):
                return dt[2]

    @property
    def sensitivity_coeff(self):
        return 83/self.ddi

    @property
    def now_coeff(self):
        return self.coeff_on_hour(datetime.now().time().hour)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def short_name(self):
        return f'{self.first_name} {self.last_name[0]}.'

    def __str__(self):
        return f'{self.full_name}'

    class Meta:
        verbose_name = _('Персона')
        verbose_name_plural = _('Персоны')
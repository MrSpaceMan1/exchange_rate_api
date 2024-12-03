import datetime

from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.
def len_equal_3(value: str):
    if len(value) > 3:
        raise ValidationError(
            _("%(value)s length is greater then 3"),
            params={"value": value}
        )

class Currency(models.Model):
    code = models.CharField(max_length=3, unique=True, validators=[len_equal_3])

    class Meta:
        verbose_name_plural = "Currencies"

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  f"{self.code}"

def date_not_in_the_future(value: datetime.date):
    if type(value) is not datetime.date:
        raise ValidationError("Value not of type datetime.date")
    if value > datetime.date.today():
        raise ValidationError("Date can't be in the future")
def rate_greater_than_zero(value: float):
    if type(value) is not float:
        raise ValidationError("Value not of type float")
    if value <= 0.0:
        raise ValidationError("Value can't be less or equal to zero")

class Rate(models.Model):
    currency_from = models.ForeignKey(
        Currency,
        db_column="currency_from",
        related_name="currency_from",
        on_delete=models.CASCADE
    )
    currency_to = models.ForeignKey(
        Currency,
        db_column="currency_to",
        related_name="currency_to",
        on_delete=models.CASCADE
    )
    date = models.DateField(validators=[date_not_in_the_future])
    rate = models.FloatField(validators=[rate_greater_than_zero])

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return  f"Rate(" \
                f"id={self.id}, " \
                f"currency_from={self.currency_from}, "\
                f"currency_to={self.currency_to}, "\
                f"date={self.date}, "\
                f"rate={self.rate})"

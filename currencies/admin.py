from django.contrib import admin
from django.db.models.aggregates import Min, Count

from .models import Currency, Rate
# Register your models here.

class CurrencyPairFilter(admin.SimpleListFilter):
    title = "possible currency to"
    parameter_name = "currency_to"

    def lookups(self, request, model_admin):
        currency_from_id = request.GET.get("currency_from__id__exact")
        currencies = (Rate.objects
                      .filter(currency_from=currency_from_id)
                      .values("currency_to")
                      .annotate(Count("currency_to"))
                      .values("currency_to", "currency_to__code"))

        return [tuple(currency.values()) for currency in currencies]

    def queryset(self, request, queryset):
        print(self.value())
        if not self.value():
            return queryset
        return queryset.filter(currency_to=self.value())

@admin.register(Rate)
class RateAdmin(admin.ModelAdmin):
    list_display = ["id", "currency_from", "currency_to", "date", "rate"]
    list_filter = [("currency_from", admin.RelatedOnlyFieldListFilter),
                   CurrencyPairFilter]

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ["id", "code"]
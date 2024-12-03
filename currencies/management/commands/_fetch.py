import datetime
import django.core.management
import yfinance
from currencies.models import Currency, Rate

ticker_codenames = ["EURUSD=X", "JPY=X", "PLN=X"]

def fetch(cls: django.core.management.BaseCommand):
    for code in ticker_codenames:
        year_ago = datetime.date.today() - datetime.timedelta(days=365)
        history = yfinance.Ticker(code).history(start=year_ago)
        close_rate = history["Close"]
        dates = history.index
        zipped = zip(dates, close_rate)
        code = code[:-2]
        from_code = "USD"
        to_code = None
        if len(code) == 6:
            from_code = code[:3]
            to_code = code[3:]
        else:
            to_code = code

        currency_from, created = Currency.objects.get_or_create(code=from_code)
        currency_to, created = Currency.objects.get_or_create(code=to_code)
        rates = [Rate(
            currency_from=currency_from,
            currency_to=currency_to,
            date=date,
            rate=rate) for date, rate in zipped]
        Rate.objects.bulk_create(rates)
        cls.stdout.write(str((from_code, to_code)))
import datetime
from django.test import TestCase
import django.db
import django.core.exceptions
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from rest_framework import status
from .models import Currency, Rate
from .views import get_currencies, get_rate


# Create your tests here.

class CurrencyTestCase(TestCase):
    def test_can_only_create_unique_currency(self):
        def add_not_unique():
            c1 = Currency(code="TST")
            c1.save()
            c2 = Currency(code="TST")
            c2.save()
        self.assertRaises(django.core.exceptions.ValidationError, add_not_unique)

    def test_code_can_be_max_3_letters(self):
        def add_too_long_code():
            c1 = Currency(code="TEST")
            c1.save()
        self.assertRaises(django.core.exceptions.ValidationError, add_too_long_code)

class CurrenciesViewsTestCase(TestCase):
    factory = APIRequestFactory()
    def test_currencies_empty(self):
        req = self.factory.get(reverse("get-currencies"))
        res = get_currencies(req)
        self.assertEqual(len(res.data), 0)

    def test_currencies_all_currencies(self):
        codes = ["USD", "EUR", "JPY", "PLN"]
        currencies = [Currency(code=x) for x in codes]
        Currency.objects.bulk_create(currencies)
        req = self.factory.get(reverse("get-currencies"))
        res = get_currencies(req)
        self.assertEqual(len(res.data), len(codes))

    def test_format_correct(self):
        c1 = Currency(code="USD")
        c1.save()
        req = self.factory.get(reverse("get-currencies"))
        res = get_currencies(req)
        self.assertEqual(res.data[0], {"code": "USD"})

    def test_order_asc(self):
        codes = ["USD", "EUR", "JPY", "PLN"]
        currencies = [Currency(code=x) for x in codes]
        Currency.objects.bulk_create(currencies)
        ordered = Currency.objects.values("code").all()
        req = self.factory.get(reverse("get-currencies")+"?order=asc")
        res = get_currencies(req)
        self.assertEqual(res.data, sorted(list(ordered), key=lambda x: x["code"]))

    def test_order_dsc(self):
        codes = ["USD", "EUR", "JPY", "PLN"]
        currencies = [Currency(code=x) for x in codes]
        Currency.objects.bulk_create(currencies)
        ordered = Currency.objects.values("code").order_by("-code").all()
        req = self.factory.get(reverse("get-currencies")+"?order=dsc")
        res = get_currencies(req)
        self.assertEqual(res.data, sorted(list(ordered), key=lambda x: x["code"], reverse=True))

    def test_allows_only_get(self):
        post_req = self.factory.post(reverse("get-currencies"))
        put_req = self.factory.put(reverse("get-currencies"))
        patch_req = self.factory.patch(reverse("get-currencies"))
        delete_req = self.factory.delete(reverse("get-currencies"))
        post_res = get_currencies(post_req)
        put_res = get_currencies(put_req)
        patch_res = get_currencies(patch_req)
        delete_res = get_currencies(delete_req)

        self.assertEqual(post_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(patch_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class RateTestCase(TestCase):
    def test_date_not_in_future(self):
        def create_rate_with_future_date():
            tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            c1, c2 = Currency(code="EUR"), Currency(code="USD")
            r1 = Rate(currency_from=c1, currency_to=c2, date=tomorrow, rate=1)
            r1.save()
        self.assertRaises(django.core.exceptions.ValidationError, create_rate_with_future_date)

    def test_rate_greater_than_zero(self):
        def create_rate_less_than_zero():
            c1, c2 = Currency(code="EUR"), Currency(code="USD")
            r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=-1)
            r1.save()
        self.assertRaises(django.core.exceptions.ValidationError, create_rate_less_than_zero)

class RateViewTestCase(TestCase):
    factory = APIRequestFactory()
    def test_bad_request_if_code_wrong(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()
        req = self.factory.get(reverse("get-rate", kwargs={"currency_from_code": c2.code, "currency_to_code": "TST"}))
        res = get_rate(req, c2.code, "TST")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_found_if_wrong_pair(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()
        req = self.factory.get(reverse("get-rate", kwargs={"currency_from_code": c2.code, "currency_to_code": c1.code}))
        res = get_rate(req, c2.code, c1.code)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_only_get_allowed(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()

        post_req = self.factory.post(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        put_req = self.factory.put(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        patch_req = self.factory.patch(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        delete_req = self.factory.delete(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        post_res = get_currencies(post_req, c1.code, c2.code)
        put_res = get_currencies(put_req, c1.code, c2.code)
        patch_res = get_currencies(patch_req, c1.code, c2.code)
        delete_res = get_currencies(delete_req, c1.code, c2.code)

        self.assertEqual(post_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(put_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(patch_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(delete_res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_ok_if_pair_correct(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()

        req = self.factory.get(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        res = get_rate(req, c1.code, c2.code)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_format_correct(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()

        req = self.factory.get(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        res = get_rate(req, c1.code, c2.code)
        self.assertEqual(res.data, {"currency_pair": f"{c1.code}{c2.code}", "exchange_rate": 1.05})

    def test_newest_rate_returned(self):
        c1 = Currency(code="USD")
        c2 = Currency(code="EUR")
        Currency.objects.bulk_create([c1, c2])
        r1 = Rate(currency_from=c1, currency_to=c2, date=datetime.date.today(), rate=1.05)
        r1.save()
        yesterday = datetime.date.today() - datetime.timedelta(days=1)
        r2 = Rate(currency_from=c1, currency_to=c2, date=yesterday, rate=1.1)
        r2.save()

        req = self.factory.get(reverse("get-rate", kwargs={"currency_from_code": c1.code, "currency_to_code": c2.code}))
        res = get_rate(req, c1.code, c2.code)

        self.assertEqual(res.data["exchange_rate"], 1.05)
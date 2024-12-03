from rest_framework import status
from rest_framework.views import Request, Response
from rest_framework.decorators import api_view
from .models import Rate, Currency


# Create your views here.

@api_view(http_method_names=["GET"])
def get_rate(req: Request, currency_from_code, currency_to_code) -> Response:
    try:
        currency_from: Currency = Currency.objects.get(code=currency_from_code)
    except Currency.DoesNotExist as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": f"Currency with code {currency_to_code} not found"
        }, status.HTTP_400_BAD_REQUEST)

    try:
        currency_to: Currency = Currency.objects.get(code=currency_to_code)
    except Currency.DoesNotExist as e:
        return Response({
            "code": status.HTTP_400_BAD_REQUEST,
            "message": f"Currency with code {currency_to_code} not found"
        }, status.HTTP_400_BAD_REQUEST)

    newest_rate = (Rate.objects
                   .filter(currency_from=currency_from.id, currency_to=currency_to.id)
                   .order_by("-date")
                   .first())

    if newest_rate is None:
        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "Currency pair not found"
        }, status.HTTP_404_NOT_FOUND)

    res_dict = {
        "currency_pair": f"{currency_from_code}{currency_to_code}",
        "exchange_rate": newest_rate.rate
    }
    return Response(res_dict)

@api_view(http_method_names=["GET"])
def get_currencies(req: Request) -> Response:
    """
    Query params:

    order: Either "asc" or "dsc"
    """
    order = req.query_params.get("order") or None
    currencies = Currency.objects
    if order:
        if order == "asc":
            currencies = currencies.order_by(f"code")
        elif order == "dsc":
            currencies = currencies.order_by(f"-code")

    currencies = currencies.values("code")
    return Response(list(currencies.all()))

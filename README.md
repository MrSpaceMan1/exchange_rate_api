# A basic currency exchange database

Project was run and tested with python 3.13 and with package versions contained in 
[requirements.txt](requirements.txt) file. I make no guarantees for other versions.

## Setup

Create virtual environment and install packages from [requirements.txt](requirements.txt) 
file. Api works on locally stored data. To initialize project migrations need to be performed. 
It can be done by executing `./manage.py migrate`. The database is empty to begin with. 
To seed the database use `./manage.py fetch_exchange_data`. That will fetch 
exchange rates for EURUSD=X, PLN=X and JPY=X by default. This can be changed by 
editing ticker codes in `currencies.management.commands._fetch.py`. Api doesn't
convert between pairs that don't exist and doesn't invert pairs that do. If a pair of
USDPLN and USDJPY is provided, exchange rate won't be provided for pairs PLNJPY or 
PLNUSD

## Endpoints

`GET /currency/` - Lists all available currencies. There's no guarantee that they 
will create a pair that exists within the database. Output's currencies in a format : 
`[{"code": "USD", ...}]`. Can be ordered alphabetically by using query parameter 
`order` with value of `asc` or `dsc`. Other values will be ignored. Ex. 
`/currency/?order=asc`

`GET /currency/<from_code>/<to_code>/` - Provides latest exchange rate for currency 
pair in format `{"currency_pair": "<from_code><to_code>", "exchange_rate": 1.034}`. 
No conversion or inversion will be performed. Fetches only existing rates.

## Admin panel

To access admin panel perform migrations and create superuser using 
`./manage.py createsuperuser`. Admin panel allows to view currencies and historical rates.
Rates view allows for filtering rates. The filter only allows to pick pairs that exist.
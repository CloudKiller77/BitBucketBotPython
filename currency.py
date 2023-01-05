from datetime import datetime
from decimal import Decimal

from pytz import timezone
from pycbrf.toolbox import ExchangeRates


class ExchangeCurrency:

    _usd = str()
    _eur = str()

    def get_date_now(self) -> str:
        saratov_tz = timezone('Europe/Moscow')
        now = saratov_tz.localize(datetime.now()).strftime("%Y-%m-%d")
        return now

    def get_usd_currency(self) -> Decimal:
        rates = ExchangeRates(self.get_date_now())
        return rates['USD'].value

    def get_eur_currency(self) -> Decimal:
        rates = ExchangeRates(self.get_date_now())
        return rates['EUR'].value

    def get_currency_info(self) -> str:
        usd = self.get_usd_currency()
        eur = self.get_eur_currency()
        return 'Курс Доллара: ' + str(usd) + ' RUB\n' + \
               'Курс Евро: ' + str(eur) + ' RUB'
#
#
# if __name__ == '__main__':
#     msg = ExchangeCurrency()
#     print(msg.get_usd())

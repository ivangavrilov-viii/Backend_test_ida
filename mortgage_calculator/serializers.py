from rest_framework import serializers

from .models import BankOffer


class OfferSerializer(serializers.ModelSerializer):
    """ Сериализатор ипотечных предложений """

    monthly_payment = serializers.SerializerMethodField(method_name='get_payment', read_only=True)

    class Meta:
        model = BankOffer
        fields = ['id', 'monthly_payment', 'bank_name', 'rate_min', 'payment_min', 'payment_max', 'term_min', 'term_max']

    def get_payment(self, queryset) -> int:
        """Метод для проверки и валидации данных для расчета платежа"""

        request = self.context.get('request')
        if 'price' in request.GET and 'deposit' in request.GET and 'term' in request.GET:
            try:
                return self.amount_of_payment(queryset)
            except ValueError:
                raise _('Could not convert data to an integer.')
            except BaseException as error:
                raise f'{error}'

    def amount_of_payment(self, queryset) -> int:
        """Метод для расчета ежемесячного платежа по ипотеке"""

        try:
            request = self.context.get('request')
            price = int(request.query_params.get('price'))
            deposit = int(request.query_params.get('deposit'))
            term = int(request.query_params.get('term'))

            price -= deposit
            month_rate = queryset.rate_min / 12 / 100
            general_rate = pow((1 + month_rate), term * 12)
            payment = round(((price * month_rate * general_rate) / (general_rate - 1)))
            return payment
        except ValueError:
            raise 'Could not convert data to an integer.'
        except BaseException as error:
            raise f'{error}'

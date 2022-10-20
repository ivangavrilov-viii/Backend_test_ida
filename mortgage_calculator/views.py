from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from .models import BankOffer
from .serializers import OfferSerializer


class OfferViewSet(viewsets.ModelViewSet):
    """Класс обработчика для всей обработки запросов: GET, POST, PATCH, DEL, включая фильтрацию и порядок"""

    serializer_class = OfferSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    ordering_param = 'order'
    ordering_fields = ('rate_min', 'term_min', 'term_max', 'payment_min', 'payment_max')

    def get_queryset(self):
        queryset = BankOffer.objects.all()

        term = self.request.query_params.get('term')
        deposit = self.request.query_params.get('deposit')
        price = self.request.query_params.get('price')

        if term and deposit and price:
            try:
                term = int(term)
                deposit = int(deposit)
                price = int(price)
                amount_of_credit = int(price - deposit)
                queryset = queryset.filter(term_min__lte=term)
                queryset = queryset.filter(term_max__gte=term)
                queryset = queryset.filter(payment_max__gte=amount_of_credit)
                queryset = queryset.filter(payment_min__lte=amount_of_credit)
            except ValueError:
                raise 'Could not convert data to an integer.'
            except BaseException as error:
                raise f'{error}'

        return queryset.order_by('rate_min', 'monthly_payment')

from rest_framework.routers import DefaultRouter

from mortgage_calculator.views import OfferViewSet

router = DefaultRouter()
router.register(r'offer', viewset=OfferViewSet, basename='offers')

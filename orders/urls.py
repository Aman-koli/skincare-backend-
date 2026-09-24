from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, ReturnRequestViewSet

router = DefaultRouter()
router.register('orders', OrderViewSet, basename='order')
router.register('returns', ReturnRequestViewSet, basename='return')

urlpatterns = router.urls
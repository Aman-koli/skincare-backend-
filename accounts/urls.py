from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import RegisterView, ProfileView, AddressViewSet

router = DefaultRouter()
router.register('addresses', AddressViewSet, basename='address')

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileView.as_view(), name='profile'),
] + router.urls
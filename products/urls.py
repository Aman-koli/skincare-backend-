from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, ReviewViewSet, WishlistViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('categories', CategoryViewSet)
router.register('reviews', ReviewViewSet)
router.register('wishlist', WishlistViewSet, basename='wishlist')

urlpatterns = router.urls
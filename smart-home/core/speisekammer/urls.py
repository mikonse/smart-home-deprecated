from rest_framework import routers

from . import views

app_name = 'speisekammer'
url_regex = r'^speisekammer/'

# Create a router and register viewsets
router = routers.DefaultRouter()
router.register(r'products', views.ProductViewSet)
router.register(r'barcodes', views.BarcodeViewSet)
router.register(r'shopping-lists', views.ShoppingListViewSet)

urlpatterns = router.urls

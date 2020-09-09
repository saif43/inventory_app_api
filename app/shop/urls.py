from django.urls import path, include
from shop import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("shop", views.ShopViewSet)
router.register("warehouse", views.WarehouseViewSet)
router.register("product", views.ProductViewSet)
router.register("customer", views.CustomerViewSet)
router.register("vendor", views.VendorViewSet)
router.register("customer_transactions", views.CustomerTrasnscationViewSet)
router.register("customer_transactions_detail", views.CustomerOrderedItemsViewSet)


app_name = "shop"

urlpatterns = [
    path("", include(router.urls)),
]
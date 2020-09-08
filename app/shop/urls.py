from django.urls import path, include
from shop import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("", views.ShowViewSet)

app_name = "shop"

urlpatterns = [
    path("", include(router.urls)),
]
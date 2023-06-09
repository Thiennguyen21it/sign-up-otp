from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from demo import views

router = DefaultRouter()
router.register("api/v1/auth/users", views.UserViewSet, basename="user")
router.register("api/v1/profiles", views.UserAccountViewSet, basename="profile")
router.register("api/v1/residential-address", views.ResidentialAddressViewSet, basename="residential-address")



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
]

urlpatterns += router.urls  




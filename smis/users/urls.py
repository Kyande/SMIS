from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'users', views.UserView, basename='users')

app_name = "users"
urlpatterns = router.urls

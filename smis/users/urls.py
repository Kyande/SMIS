from django.urls import path
from rest_framework.routers import SimpleRouter

from . import views


router = SimpleRouter()
router.register(r'users', views.UserView)

urlpatterns = router.urls

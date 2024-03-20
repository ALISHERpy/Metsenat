from django.urls import path,include
from .views import SponsorListView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('SponsorListView', SponsorListView, 'StudentViewSet1')

urlpatterns = [
    path('', include(router.urls)),


]
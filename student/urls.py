from django.urls import path, include
from .views import DashboardStat, StudentsViewSet, SponsorshipView, SponsorshipDetailView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("StudentView",StudentsViewSet,'forstudents')


urlpatterns = [
    path('',include(router.urls)),
    path('dashboard/', DashboardStat.as_view()),
    path('sponsorships', SponsorshipView.as_view(), name='sponsorships'),
    path('sponsorships/<int:pk>', SponsorshipDetailView.as_view(), name='sponsorship-detail'),

]
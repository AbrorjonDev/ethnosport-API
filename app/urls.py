from django.urls import path, include
from rest_framework.routers import DefaultRouter


from .views import *


app_name = 'app'

router = DefaultRouter()

router.register(r'regions', RegionsViewSet)
router.register(r'sports', SportsViewSet)
router.register(r'sport-images', SportImagesViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'sportsmen', SportsmenViewSet)
router.register(r'sportsmen-images', SportsmenImagesViewSet)
router.register(r'events', EventsViewSet)
router.register(r'competitions', CompetitionsViewSet)
router.register(r'competition-images', CompetitionImagesViewSet, basename='competitionimages')

urlpatterns = [
    path('', include(router.urls)),
]


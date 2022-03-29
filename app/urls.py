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
router.register(r'sportsmenimages', SportsmenImagesViewSet)
router.register(r'events', EventsViewSet)
router.register(r'competitions', CompetitionsViewSet)
router.register(r'competitionimages', CompetitionImagesViewSet)
router.register(r'comments', CommentsINCompetitionsViewSet)
router.register(r'fotos', FotosViewSet)
router.register(r'videos', VideosViewSet)
router.register(r'categorydocs', CategoryDocsViewSet)
router.register(r'docs',DocsViewSet)
router.register(r'news', NewsViewSet)
# router.register(r'newsimages', )
router.register(r'appeals/get', AppealsReadViewSet)
router.register(r'appeals/post', AppealsPostViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


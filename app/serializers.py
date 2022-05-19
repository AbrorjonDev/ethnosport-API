from email.policy import default
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.postgres.validators import ArrayMaxLengthValidator


User = get_user_model()

from .models import *


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class SportsmenForOthersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sportsmen
        fields = ('url', 'pk', 'name')
        extra_kwargs = {
            'url':{'view_name':'app:sportsmen-detail', 'lookup_field':'pk'},
        }


class EventsForOthersSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Events
        fields = ('url', 'pk', 'name')
        extra_kwargs = {
            'url':{'view_name':'app:events-detail', 'lookup_field':'pk'},
        }

class RegionListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    admin = UserSerializer(required=False)
    get_sportsmen = SportsmenForOthersSerializer(many=True, required=False, read_only=True)
    get_events = SportsmenForOthersSerializer(many=True, required=False, read_only=True)
    statistics = serializers.FloatField(required=False, read_only=True)
    get_sportsmen_count = serializers.IntegerField(required=False, read_only=True)
    get_events_count = serializers.IntegerField(required=False,read_only=True)

    class Meta:
        model = RegionModel
        fields = ['url', 'id', 'name', 'email', 'admin', 'phone','boss', 'address', 'd', 'reg_id', 'date_created', 'date_updated', 'get_sportsmen', 'get_events', 'statistics', 'get_sportsmen_count', 'get_events_count']
        extra_kwargs = {
            'url':{'view_name':'app:regionmodel-detail', 'lookup_field':'pk'}, 
            'd':{'read_only':True},
            'reg_id':{'read_only':True},
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True}
        }


class RegionSerializer(serializers.ModelSerializer):
    get_sportsmen = SportsmenForOthersSerializer(many=True, required=False, read_only=True)
    get_events = SportsmenForOthersSerializer(many=True, required=False, read_only=True)
    statistics = serializers.FloatField(required=False, read_only=True)
    get_sportsmen_count = serializers.IntegerField(required=False, read_only=True)
    get_events_count = serializers.IntegerField(required=False, read_only=True)
    class Meta:
        model = RegionModel
        fields = ['id', 'name', 'email', 'admin', 'phone','boss', 'address', 'd', 'reg_id', 'date_created', 'date_updated', 'get_sportsmen', 'get_events', 'statistics', 'get_sportsmen_count', 'get_events_count']
        extra_kwargs = {
            # 'url':{'view_name':'app:regionmodel-detail', 'lookup_field':'pk'}, 
            'd':{'read_only':True},
            'reg_id':{'read_only':True},
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }

class RegionForOtherSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = RegionModel
        fields = ['url', 'id', 'name', 'phone']
        extra_kwargs = {
            'url':{'view_name':'app:regionmodel-detail', 'lookup_field':'pk'}, 
        }
    



class SportsSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sports
        fields = ['pk', 'url','pk', 'name', 'text']
        extra_kwargs = {
            'url':{'view_name':'app:sports-detail', 'lookup_field':'pk'}, 
            'pk':{'read_only':True},
        }


class SportIMGObjectSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    sport = SportsSerializer(required=False)
    url = serializers.HyperlinkedIdentityField(view_name='app:sportimages-detail', lookup_field='pk')
    class Meta:
        model = SportImages
        fields = ("url", "image", "sport")

class SportImagesSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = SportImages
        fields = ['url', 'image',]
        extra_kwargs = {
            'url':{ 'view_name':'app:sportimages-detail', 'lookup_field':'pk'}
        }
       


class SportsListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    sport_images = SportImagesSerializer(required=False, many=True)
    class Meta:
        model = Sports
        fields = ['url','id', 'name',  'slug', 'date_created', 'date_updated', 'sport_images', 'text']
        extra_kwargs = {
            'url':{'view_name':'app:sports-detail', 'lookup_field':'pk'}, 
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }


class SportWithImagesSerializer(serializers.Serializer):
    sport = serializers.CharField()
    images = serializers.ImageField()
    text = serializers.CharField(max_length=20000, required=False, allow_blank=True)


class CategorySerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['url','id', 'name']
        extra_kwargs = {
            'url':{'view_name':'app:category-detail', 'lookup_field':'pk', 'read_only':True}, 
        }


class SportsmenImagesForOtherSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SportsmenImages
        fields = ('url', 'pk', 'image',)
        extra_kwargs = {
            'url':{'view_name':'app:sportsmenimages-detail', 'lookup_field':'pk'}
        }

class SportsmenSerializer(serializers.ModelSerializer):
    sportsman_images = SportsmenImagesForOtherSerializer(required=False, many=True)
    # images = serializers.ImageField(required=False)
    class Meta:
        model = Sportsmen
        fields = ['id', 'name', 'date', 'achievements', 'category','sport', 'region', 'sportsman_images', ]
        extra_kwargs = {
            'id': {'read_only':True},
            'sportsman_images':{'read_only':True}
            }

class SportsmenListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    category = CategorySerializer(required=False, many=True)
    sport = SportsSerializer(required=False, many=False)
    region = RegionForOtherSerializer(required=False)
    sportsman_images = SportsmenImagesForOtherSerializer(required=False, many=True)
    class Meta:
        model = Sportsmen
        fields = ['url', 'id', 'name', 'date', 'achievements', 'category','sport', 'region', 'sportsman_images']
        extra_kwargs = {
            'url':{'view_name':'app:sportsmen-detail', 'lookup_field':'pk'}, 
            'sportsman_images':{'read_only':True}
            }
        depth = 1


class SportsmenCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    date = serializers.DateField()
    achievements = serializers.ListField(allow_null=True, child=serializers.CharField(label='Achievements', style={'base_template': 'textarea.html'}), required=False, validators=[ArrayMaxLengthValidator])
    images = serializers.ImageField()


class SportsmenImagesSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='app:sportsmenimages-detail', lookup_field='pk')

    class Meta:
        model = SportsmenImages
        fields = ('url', 'id', 'image', )
        

class EventsForOtherSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventsImages
        fields = ('pk', 'image')


class EventsListSerializer(serializers.HyperlinkedModelSerializer):
    get_images = EventsForOtherSerializer(required=False, many=True, read_only=True)
    region = RegionForOtherSerializer(required=False)
    class Meta:
        model = Events
        fields = (
            'url', 'id','name', 'text','videos','get_images', 'seen', 'rate','visited', 'region', 'date_occured', 'date_created','date_updated'
            )
        extra_kwargs = {
            'url':{'view_name':'app:events-detail', 'lookup_field':'pk'},
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
            'visited':{'read_only':True},
        }

class EventsSerializer(serializers.ModelSerializer):
    get_images = EventsForOtherSerializer(required=False, many=True, read_only=True)
    images = serializers.ImageField(required=False, write_only=True)
    class Meta:
        model = Events
        fields = ('pk','text','name', 'videos','get_images', 'seen', 'rate','visited', 'region', 'date_occured', 'date_created','date_updated', 'images')
        extra_kwargs = {
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
            'visited':{'read_only':True},
        }

class CISerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionImages
        fields = ('pk', 'image', 'competition')

class CompetitionImagesListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompetitionImages
        fields = ('pk', 'image')


class CompetitionsListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    # sports = SportsSerializer(required=False)
    region = RegionForOtherSerializer(required=False)
    #main_competition_image = serializers.ImageField()
    class Meta:
        model = Competitions
        fields = ('url', 'id', 'name', 'pdf','image', 'region', 'download_counter')
        extra_kwargs = {
            'url':{'view_name':'app:competitions-detail', 'lookup_field':'pk', 'read_only':True},
        }
        depth=1



class CommentsINCompetitionsListSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CommentsINCompetitions
        fields = ('url', 'pk', 'comment', 'name', 'date_created')

        extra_kwargs = {
            'url':{'view_name':'app:commentsincompetitions-detail', 'lookup_field':'pk'},
            
        }



class CompetitionsSerializer(serializers.ModelSerializer):
    #competition_images = CompetitionImagesListSerializer(many=True, required=False)
    sports = SportsSerializer(many=True)
    get_comments = CommentsINCompetitionsListSerializer(many=True)

    class Meta:
        model = Competitions
        fields = ('id', 'name', 'sports', 'pdf','region', 'image', 'get_comments', 'download_counter')#'competition_images'


class CommentsINCompetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsINCompetitions
        fields = ('pk', 'comment', 'name', 'competition', )

        extra_kwargs = {
            'pk':{'read_only':True},            
        }


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = "__all__"



class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = "__all__"

class DocsSerializer(serializers.ModelSerializer):
    # category = CategoryDocsSerializer(many=True, required=False)

    class Meta:
        model = Docs
        fields = ('pk', 'name', 'category', 'doc', 'doc_url')


class CategoryDocsSerializer(serializers.ModelSerializer):
    get_docs = DocsSerializer(many=True, required=False)
    class Meta:
        model = CategoryDocs
        fields = ('pk', 'name', 'get_docs')


class NewsImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsImages
        fields = ('pk', 'image',)

class NewsSerializer(serializers.ModelSerializer):
    news_images = NewsImagesSerializer(required=False, many=True, read_only=True)
    images = serializers.ImageField(required=False)
    main_image = NewsImagesSerializer(required=False, many=False, read_only=True)
     
    class Meta:
        model = News
        fields = ('pk', 'name', 'title', 'news_images','images', 'main_image', 'date_added', 'date_updated',)

        extra_kwargs = {
            
        }

    
class AppealsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appeals
        fields = "__all__"

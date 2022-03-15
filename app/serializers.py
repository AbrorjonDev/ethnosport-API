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


class RegionListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    admin = UserSerializer(required=False)
    class Meta:
        model = RegionModel
        fields = ['url', 'id', 'name', 'email', 'admin', 'phone','boss', 'address', 'd', 'reg_id', 'date_created', 'date_updated']
        extra_kwargs = {
            'url':{'view_name':'app:regionmodel-detail', 'lookup_field':'pk'}, 
            'd':{'read_only':True},
            'reg_id':{'read_only':True},
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegionModel
        fields = ['id', 'name', 'email', 'admin', 'phone','boss', 'address', 'd', 'reg_id', 'date_created', 'date_updated']
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
        fields = ['pk', 'url','pk', 'name']
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
        fields = ['url','id', 'name',  'slug', 'date_created', 'date_updated', 'sport_images']
        extra_kwargs = {
            'url':{'view_name':'app:sports-detail', 'lookup_field':'pk'}, 
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }


class SportWithImagesSerializer(serializers.Serializer):
    sport = serializers.CharField()
    images = serializers.ImageField()



class CategorySerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['url','id', 'name']
        extra_kwargs = {
            'url':{'view_name':'app:category-detail', 'lookup_field':'pk', 'read_only':True}, 
        }


class SportsmenSerializer(serializers.ModelSerializer):
    # images = serializers.ImageField(required=False)
    class Meta:
        model = Sportsmen
        fields = ['id', 'name', 'date', 'achievements', 'category','sport', 'region', 'sportsman_images', ]
        extra_kwargs = {
            # 'url':{'view_name':'app:regionmodel-detail', 'lookup_field':'pk'}, 
            'id': {'read_only':True},
            'sportsman_images':{'read_only':True},
            # 'images': {'write_only':True},   
            }

class SportsmenListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    category = CategorySerializer(required=False, many=True)
    sport = SportsSerializer(required=False, many=False)
    region = RegionForOtherSerializer(required=False)

    class Meta:
        model = Sportsmen
        fields = ['url', 'id', 'name', 'date', 'achievements', 'category','sport', 'region', 'main_sportman_image']
        extra_kwargs = {
            'url':{'view_name':'app:sportsmen-detail', 'lookup_field':'pk'}, 
            'id':{'read_only':True},
            'main_sportman_image':{'read_only':True}
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
        # extra_kwargs = { 
        #     'url':{'view_name':'app:sportsmenimages-detail', 'lookup_field':'pk', 'read_only':True},
        # }


class EventsListSerializer(serializers.HyperlinkedModelSerializer):
    
    region = RegionForOtherSerializer(required=False)
    class Meta:
        model = Events
        fields = (
            'url', 'id','text','videos','seen', 'rate','region', 'date_occured', 'date_created','date_updated'
            )
        extra_kwargs = {
            'url':{'view_name':'app:events-detail', 'lookup_field':'pk'},
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }

class EventsSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    
    # region = RegionForOtherSerializer(required=False)
    class Meta:
        model = Events
        fields = "__all__"
        extra_kwargs = {
            'date_created':{'read_only':True},
            'date_updated':{'read_only':True},
        }

class CISerializer(serializers.ModelSerializer):
    class Meta:
        model = CompetitionImages
        fields = ('pk', 'image', 'competition')

class CompetitionImagesListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CompetitionImages
        fields = ('pk', 'image')

        # extra_kwargs = {
        #     'url':{'view_name':'apps:competitionimages-detail', 'lookup_field':'pk'}
        # }




class CompetitionsListSerializer(serializers.HyperlinkedModelSerializer, serializers.ModelSerializer):
    # sports = SportsSerializer(required=False)
    # region = RegionForOtherSerializer(required=False)
    main_competition_image = serializers.ImageField()
    class Meta:
        model = Competitions
        fields = ('url', 'id', 'name', 'pdf', 'main_competition_image')
        extra_kwargs = {
            'url':{'view_name':'app:competitions-detail', 'lookup_field':'pk', 'read_only':True},
        }
        depth=1



class CommentsINCompetitionsListSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = CommentsINCompetitions
        fields = ('url', 'pk', 'comment', 'name', 'rate')

        extra_kwargs = {
            'url':{'view_name':'app:commentsincompetitions-detail', 'lookup_field':'pk'},
            
        }



class CompetitionsSerializer(serializers.ModelSerializer):
    competition_images = CompetitionImagesListSerializer(many=True, required=False)
    sports = SportsSerializer(many=True)
    get_comments = CommentsINCompetitionsListSerializer(many=True)

    class Meta:
        model = Competitions
        fields = ('id', 'name', 'sports', 'pdf', 'competition_images', 'get_comments')
        
    extra_kwargs = {
        'competition_images':{'read_only':True},
        'images':{'write_only':True},
    }

class CommentsINCompetitionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentsINCompetitions
        fields = ('pk', 'comment', 'name', 'competition', 'rate')

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

class DocsSerializer(serializers.HyperlinkedModelSerializer):
    # category = CategoryDocsSerializer(many=True, required=False)

    class Meta:
        model = Docs
        fields = ('pk', 'url', 'name', 'category', 'doc', 'doc_url')

        extra_kwargs = {
            'view_name':'app:docs-detail',
            'lookup_field':'pk',
            'read_only':True
        }



class CategoryDocsSerializer(serializers.HyperlinkedModelSerializer):
    get_docs = DocsSerializer(many=True, required=False)
    url = serializers.HyperlinkedIdentityField(view_name='app:categorydocs-detail', lookup_field='pk', source=CategoryDocs)
    class Meta:
        model = CategoryDocs
        fields = ('pk', 'url', 'name', 'get_docs')

        extra_kwargs = {
            'view_name':'app:categorydocs-detail',
            'lookup_field':'pk',
        }


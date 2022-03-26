from django.conf import settings
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination 
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny

from .models import *

from .serializers import *


class RegionsViewSet(ModelViewSet):
    queryset = RegionModel.objects.all()
    serializer_class = RegionSerializer
    list_serializer_class = RegionListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get_queryset(self):
        return RegionModel.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.list_serializer_class(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)



class SportsViewSet(ModelViewSet):
    queryset = Sports.objects.all()
    serializer_class = SportsSerializer
    list_serializer_class = SportsListSerializer

    def get_queryset(self):
        return Sports.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.list_serializer_class(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)

    def create(self, request):
        serializer = SportWithImagesSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # serializer.save()
            sport = serializer.validated_data.get('sport')
            try:
                sport_obj = Sports.objects.create(name=sport)
            except Exception as e:
                raise e
            try:
                images = request.FILES.getlist('images')
                for img in images:
                    SportImages.objects.create(sport=sport_obj, image=img)
            except Exception as e:
                raise e
            data = SportsListSerializer(Sports.objects.last(), many=False, context={'request':request}).data
            return Response(data, status=201)
        return Response(serializer.errors, status=400)


class SportImagesViewSet(ModelViewSet):
    queryset = SportImages.objects.all()
    serializer_class = SportIMGObjectSerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    """
        This Category API is for sportsmen.  
    """


class SportsmenViewSet(ModelViewSet):
    queryset = Sportsmen.objects.all()
    serializer_class = SportsmenSerializer
    # pagination_class = LimitOffsetPagination
    # page_size=100

    def get_queryset(self, region=None, sport=None, category=None):
        if category:
            category_obj = get_object_or_404(Category, pk=category)
            category = category_obj
        if region and sport and category:
            return Sportsmen.objects.filter(region_id=region, sport_id=sport, category=category )
        elif region and sport:
            return Sportsmen.objects.filter(region_id=region, sport_id=sport)
        elif sport and category:
            return Sportsmen.objects.filter(sport_id=sport, category_id=category)
        elif category and region:
            return Sportsmen.objects.filter(region_id=region, category_id=category)
        elif region:
            return Sportsmen.objects.filter(region_id=region)
        elif category:
            return Sportsmen.objects.filter(category_id=category)
        elif sport:
            return Sportsmen.objects.filter(sport_id=sport)
        else:
            return Sportsmen.objects.all()


    def list(self, request):
        region=request.GET.get('r', None)
        category=request.GET.get('c', None)
        sport=request.GET.get('s', None)
        queryset = self.get_queryset(region=region, category=category, sport=sport)
        serializer = SportsmenListSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)


    def create(self, request):
        serializer = SportsmenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            name, date = data['name'], data['date']
            category, sport = data['category'], data['sport']
            region, achievements = data['region'], data['achievements']
            sportsman_obj = Sportsmen.objects.create(
                name=name, date=date, achievements=achievements,
                sport=sport, region=region,
                )
            sportsman_obj.category.set(category)
            sportsman_obj.save()

            images = request.FILES.getlist('images')
            for img in images:
                SportsmenImages.objects.create(sportsman=sportsman_obj, image=img)
            # data = SportsmenSerializer(sportsman_obj, many=False).data
            return Response({'status':'created'}, status=200)
        return Response(serializer.errors, status=400)


class SportsmenImagesViewSet(ModelViewSet):
    queryset = SportsmenImages.objects.all()
    serializer_class = SportsmenImagesSerializer


    def list(self, request):
        queryset = SportsmenImages.objects.all()
        # page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)
        # return self.get_paginated_response(serializer.data)



class EventsViewSet(ModelViewSet):
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

    def get_queryset(self, region=None):
        if region:
            return Events.objects.filter(region_id=region)
        return Events.objects.all()

    def list(self, request):
        region = request.GET.get('r', None)
        queryset = self.get_queryset(region=region)
        serializer = EventsListSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)
    
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.visited += 1
        obj.save() 
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)


    # def retrieve(self, request, *args, **kwargs):
    #     print("retrieve working..")
    #     obj = self.get_object()
    #     serializer = self.serializer_class(obj, data=request.data, partial=True)
    #     if serializer.is_valid(raise_exception=True):
    #         if serializer.validated_data.get('read'):
    #             print(serializer.validated_data.get('read'))
    #             obj.visited += 1
    #             obj.save()
    #         serializer.save()
    #         print("properly working..")
    #         return Response(serializer.data, status=200)
    #     return Response(serializer.errors, status=400)
        

class CompetitionsViewSet(ModelViewSet):
    queryset = Competitions.objects.all()
    serializer_class = CompetitionsSerializer

    def get_queryset(self, sport=None):
        if sport:
            return Competitions.objects.filter(sports__in=sport)
        return Competitions.objects.all()

    def list(self, request):
        sport = request.GET.get('s', None)
        queryset = self.get_queryset(sport=sport)
        serializer = CompetitionsListSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data, status=200)
    

    def create(self, request):
        serializer = CompetitionsSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            name, sports = data['name'], data['sports']
            pdf = data['pdf']
            
            competition_obj = Competitions.objects.create(
                name=name, pdf=pdf
                )
            competition_obj.sports.set(sports)
            competition_obj.save()

            images = request.FILES.getlist('images')
            for img in images:
                CompetitionImages.objects.create(competition=competition_obj, image=img)
            # data = SportsmenSerializer(sportsman_obj, many=False).data
            return Response({'status':'created'}, status=200)
        return Response(serializer.errors, status=400)


class CompetitionImagesViewSet(ModelViewSet):
    queryset = CompetitionImages.objects.all()
    serializer_class = CISerializer #CompetitionImagesListSerializer


class CommentsINCompetitionsViewSet(ModelViewSet):
    queryset = CommentsINCompetitions.objects.all()
    serializer_class = CommentsINCompetitionsSerializer

    

class VideosViewSet(ModelViewSet):
    queryset = Videos.objects.all()
    serializer_class=VideosSerializer


class FotosViewSet(ModelViewSet):
    queryset = Fotos.objects.all()
    serializer_class=FotosSerializer


class CategoryDocsViewSet(ModelViewSet):
    queryset = CategoryDocs.objects.all()
    serializer_class = CategoryDocsSerializer

class DocsViewSet(ModelViewSet):
    queryset = Docs.objects.all()
    serializer_class = DocsSerializer

    

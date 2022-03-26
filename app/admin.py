from django.contrib import admin

from app.views import CommentsINCompetitionsViewSet

from .models import *


class SportsmenInline(admin.StackedInline):
    model = Sportsmen
    classes = ('collapse',)

    def queryset(request):
        return Sportsmen.objects.filter(region=request.user.regionmodel)

class EventsInline(admin.StackedInline):
    model = Events
    classes = ('collapse',)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'admin', 'phone')
    search_fields = ('name', 'phone', 'email', 'admin__username')

    fieldsets = (
        (None, {
            'fields':('name', ('admin', 'boss'))
        }),
        ('CONTACTS', {
            'fields':('email', 'phone'),
            'classes':('collapse',)
        }),
        ('ADDRESS', {
            'fields':('address', 'd', 'reg_id'),
            'classes':('collapse',),

        }),
    )

    def save_model(self, request, obj, form, change) -> None:
        if getattr(obj, 'admin', None) is None:
            obj.admin = request.user
        obj.save()
        return super().save_model(request, obj, form, change)


    inlines = [
        SportsmenInline, EventsInline
    ]

admin.site.register(RegionModel, RegionAdmin)

class SportImagesInline(admin.StackedInline):
    classes = ('collapse',)
    model = SportImages


class SportsAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    fields = ('name',)
    list_display = ('name', 'date_created', 'date_updated')

    inlines = [
        SportImagesInline,
        ]
admin.site.register(Sports,SportsAdmin)


admin.site.register(SportImages)

class SportsmenImagesInline(admin.StackedInline):
    classes = ('collapse',)
    model = SportsmenImages

class SportsmenAdmin(admin.ModelAdmin):
    list_display = ('name', 'region', 'sport')
    search_fields = ('name', 'region__name', 'sport__name')

    filter_horizontal = ('category',)

    inlines = [SportsmenImagesInline]

admin.site.register(Sportsmen, SportsmenAdmin)

admin.site.register(Category)


admin.site.register(SportsmenImages)


admin.site.register(Events)

class CompetitionImagesINline(admin.StackedInline):
    model = CompetitionImages
    classes = ('collapse',)

class CompetitionCommentsINline(admin.StackedInline):
    model = CommentsINCompetitions
    classes = ('collapse',)

class CompetitionsAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'sports')
    
    filter_horizontal = ('sports',)

    inlines = [CompetitionImagesINline, CompetitionCommentsINline]


admin.site.register(Competitions, CompetitionsAdmin)

admin.site.register(CommentsINCompetitions)

admin.site.register(Videos)

admin.site.register(Fotos)

admin.site.register(CategoryDocs)

admin.site.register(Docs)


class NewsImagesInline(admin.StackedInline):
    model = NewsImages
    classes = ('collapse',)


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

    inlines = [NewsImagesInline]

admin.site.register(NewsImages)

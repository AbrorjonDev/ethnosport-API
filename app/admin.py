from django.contrib import admin

from .models import *
# Register your models here.
admin.site.register(RegionModel)

admin.site.register(Sports)


admin.site.register(SportImages)

admin.site.register(Sportsmen)

admin.site.register(Category)


admin.site.register(SportsmenImages)


admin.site.register(Events)

admin.site.register(Competitions)

admin.site.register(CommentsINCompetitions)

admin.site.register(Videos)

admin.site.register(Fotos)

admin.site.register(CategoryDocs)

admin.site.register(Docs)

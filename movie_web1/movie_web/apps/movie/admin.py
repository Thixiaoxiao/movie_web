from django.contrib import admin

# Register your models here.
from movie import models

admin.site.register(models.Movie)
admin.site.register(models.CateGory)
admin.site.register(models.Connection_Movie_Category)
admin.site.register(models.Connection_Movie_Actor)
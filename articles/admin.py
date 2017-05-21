from django.contrib import admin
from . import models
# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
	list_display = ['id','user','source','image','title','created']

class ProfileAdmin(admin.ModelAdmin):
	list_display = ['id','user','photo']

admin.site.register(models.Article, ArticlesAdmin)
admin.site.register(models.Profile, ProfileAdmin)
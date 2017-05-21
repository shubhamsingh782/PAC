from django.contrib import admin
from . import models
# Register your models here.
class ArticlesAdmin(admin.ModelAdmin):
	list_display = ['id','user','source','image','title','created']


admin.site.register(models.Article, ArticlesAdmin)
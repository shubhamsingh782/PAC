from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


# Create your models here
		
class Article(models.Model):
	user = models.ForeignKey(User, related_name='scraped_article')
	source = models.URLField(max_length=500 ,blank=False, null=False)
	image = models.URLField(max_length=500,blank=True, null=True)
	title = models.CharField(max_length=200, blank=False)
	slug = models.SlugField(max_length=250, unique_for_date='created')
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ('created',)

	def __str__(self):
		return self.title


class Profile(models.Model):
	user = models.OneToOneField(User, related_name='user_image', default=User.objects.get(username="shubham"))
	photo = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True)

	def __str__(self):
		return 'Profile For {}'.format(self.request.user)
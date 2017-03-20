from rest_framework import serializers
from django.contrib.auth.models import User
from articles.models import Article
#from django.contrib.auth import get_user_model

class UserRegistrationSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password')

		extra_kwargs = {'password':{'write_only':True}}

	def create(self, validated_data):
		user_obj = User(
				username=validated_data['username'],
				first_name=validated_data['first_name'],
				last_name=validated_data['last_name'],
				email = validated_data['email']
				)
		user_obj.set_password(validated_data['password'])
		user_obj.save()
		return validated_data

class UserLoginSerializer(serializers.ModelSerializer):
	token = serializers.CharField(allow_blank=False, read_only=True)
	class Meta:
		model = User
		fields = ('username','password','token')

		extra_kwargs = {'password':{'write_only':True}}

class ArticleCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('source',)

class ArticleListSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='api_articles:details')
	class Meta:
		model = Article
		fields = ('url','title',)

			
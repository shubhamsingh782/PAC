from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from articles.models import Article
from rest_framework.validators import UniqueValidator
#from django.contrib.auth import get_user_model

#DELETE_URL = serializers.HyperlinkedIdentityField(view_name='api_articles:delete')

class PasswordResetSerializer(serializers.Serializer):
	email_or_username = serializers.CharField(required=True, max_length=100)

class UsernameAvailability(serializers.Serializer):
	username = serializers.CharField(required=True, max_length=32)

class EmailAvailability(serializers.Serializer):
	email = serializers.CharField(required=True, max_length=100)

class SetPasswordSerializer(serializers.Serializer):
	password = serializers.CharField(required=True, max_length=50)

class UserRegistrationSerializer(serializers.ModelSerializer):
	email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
	first_name = serializers.CharField(required=True, max_length=100)
	last_name = serializers.CharField(required=True, max_length=100)
	class Meta:
		model = User
		fields = ('username','first_name','last_name','email','password')

		extra_kwargs = {'password':{'write_only':True}}



class UserLoginSerializer(serializers.ModelSerializer):
	username = serializers.CharField(required=True)
	password = serializers.CharField(required=True, style={'input_type': 'password'})
	#token = serializers.CharField(allow_blank=False, read_only=True)
	class Meta:
		model = User
		fields = ('username','password',)

		extra_kwargs = {'password':{'write_only':True}}

	def validate(self,attrs):
		username = attrs.get('username')
		password = attrs.get('password')

		if username and password:
			user = authenticate(username=username, password=password)

			if not user:
				raise serializers.ValidationError({'message':'Invalid credentials'}, code='authorization')
		else:
			raise serializers.ValidationError({'message':'please enter username and password both'}, code='authorization')

		attrs['user']=user
		return attrs


class ArticleCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Article
		fields = ('source',)

class ArticleListSerializer(serializers.ModelSerializer):
	url=serializers.HyperlinkedIdentityField(view_name='api_articles:detail')
	class Meta:
		model = Article
		fields = ('id','url','title','image',)


class ArticleDetailSerializer(serializers.ModelSerializer):
	url = serializers.HyperlinkedIdentityField(view_name='api_articles:delete')
	success = serializers.BooleanField
	class Meta:
		model = Article
		fields = ('source','title','content','created','url','image',)
from .serializers import(
	UserRegistrationSerializer,
	UserLoginSerializer,
	ArticleCreateSerializer,
	ArticleListSerializer,
	ArticleDetailSerializer,
	)
from rest_framework.generics import(
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView,
	DestroyAPIView,
	)
from .permissions import IsOwner
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.views import APIView
from articles.models import Article
from django.contrib import auth
from rest_framework.authtoken.models import Token
from newspaper import Article as page
from bs4 import BeautifulSoup
from urllib.request import FancyURLopener
from random import choice

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9'
]

class MyOpener(FancyURLopener):
	version = choice(user_agents)

urlopen = MyOpener().open

def scrape(url):
	html = urlopen(url)
	art = BeautifulSoup(html.read(),'html.parser')
	title = art.title.text

	try:
		article = page(url)
		article.download()
		article.parse()
		content = article.text
		image = article.top_image
	except:
		image = ''
		content = ""
		for para in art.find_all('p'):
			content+='\n'
			content+=para.text
	
	if image == None or image=='':
		link=art.find('img')
		src = link['src']
		if 'https' or 'http' in src:
			image=src
		elif '//' in src:
			image = 'https:'+src
		else:
			sublist = url.split('/')
			if src[0]=='/':
				image='https://'+sublist[2]+src
			else:
				image='https://'+sublist[2]+'/'+src

			
	return title, content, image

class UserRegistrationAPIView(CreateAPIView):
	serializer_class = UserRegistrationSerializer
	queryset = User.objects.all()

class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		if not serializer.is_valid():
			return Response({'status':False,'message':"Invalid Credentials"}, status=HTTP_400_BAD_REQUEST)

		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		if user:
			return Response(
						{'status':True,
							 "message":"successfully logged in",
							 'token':token.key,
							 'username':user.username,
							 'name':user.first_name+" "+user.last_name,
							 'email':user.email
							 },
						 status=HTTP_200_OK)
		return Response({'status':False,'message':"Invalid credentials"}, status=HTTP_400_BAD_REQUEST)

class ArticleCreateAPIView(CreateAPIView):
	serializer_class = ArticleCreateSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		url=self.request.POST.get('source')
		title, content, image = scrape(url)
		serializer.save(user=self.request.user,title=title,content=content,image=image)

class ArticleListAPIView(ListAPIView):
	serializer_class = ArticleListSerializer
	permission_classes = [IsAuthenticated]

	def get_queryset(self):
		articles = Article.objects.all().filter(user=self.request.user)
		return articles

class ArticleDetailAPIView(RetrieveAPIView):
	serializer_class = ArticleDetailSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated, IsOwner]

class ArticleDeletAPIView(APIView):
	serializer_class = ArticleDetailSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated, IsOwner]

	def get_object(self, pk):
		try:
			article = Article.objects.get(pk=pk)
		except ObjectDoesNotExist:
			article = None

		return article

	def perform_destroy(self, instance):
		if instance:
			
			if self.request.user != instance.user:
				return Response({'status':False, 'message':'You Do Not have permission to Delete This object'}, status=HTTP_400_BAD_REQUEST)
			
			instance.delete()			
			return Response({'status':True, 'message':'Content Deleted SuccessFully'}, status=HTTP_200_OK)
		
		return Response({'status':False, 'message':'No Such Content Found To delete'}, status=HTTP_400_BAD_REQUEST)



	def destroy(self, request, pk, *args, **kwargs):
		obj = self.get_object(pk)
		return self.perform_destroy(obj)

	def delete(self, request, pk, *args, **kwargs):
		return self.destroy(request, pk, *args, **kwargs)


class APILogout(APIView):
	queryset = User.objects.all()
	permission_classes = [IsAuthenticated,]

	def get(self,request):
			request.user.auth_token.delete()
			auth.logout(request)
			return Response({'status':True,'message': 'SuccessFully Logged Out'}, status=HTTP_200_OK)

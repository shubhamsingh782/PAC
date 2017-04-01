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
from rest_framework.views import APIView
from articles.models import Article
from django.contrib import auth
from rest_framework.authtoken.models import Token
from newspaper import Article as page
from bs4 import BeautifulSoup
from urllib.request import urlopen

def scrape(url):
	try:
		article = page(url)
		article.download()
		article.parse()
		title = article.title
		content = article.text
	except:
		html = urlopen(url)
		article = BeautifulSoup(html.read(),'html.parser')
		title = article.title.text
		content = ""
		for para in article.find_all('p'):
			content+=para.text
			content+='\n'
			
	return title,content

class UserRegistrationAPIView(CreateAPIView):
	serializer_class = UserRegistrationSerializer
	queryset = User.objects.all()

class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	permission_classes = [AllowAny]

	def post(self, request, *args, **kwargs):
		data = request.data
		serializer = UserLoginSerializer(data=data)
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		if user:
			return Response(serializer.data, status=HTTP_200_OK)
		return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

class ArticleCreateAPIView(CreateAPIView):
	serializer_class = ArticleCreateSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated,]

	def perform_create(self,serializer):
		url=self.request.POST.get('source')
		title,content = scrape(url)
		serializer.save(user=self.request.user,title=title,content=content)

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

class ArticleDeletAPIView(DestroyAPIView):
	serializer_class = ArticleDetailSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated, IsOwner]

class APILogout(APIView):
	queryset = User.objects.all()
	permission_classes = [IsAuthenticated,]

	def get(self,request):
		request.user.auth_token.delete()
		auth.logout(request)
		return Response({'success': 'SuccessFully Logged Out'}, status=HTTP_200_OK)
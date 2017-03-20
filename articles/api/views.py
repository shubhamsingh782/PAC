from .serializers import(
	UserRegistrationSerializer,
	UserLoginSerializer,
	ArticleCreateSerializer,
	ArticleListSerializer
	)
from rest_framework.generics import(
	CreateAPIView,
	ListAPIView,
	RetrieveAPIView
	)
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from articles.models import Article

def scrape(url):
	title="hey"
	content = "hllo there here im"
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
		if serializer.is_valid():
			new_data = serializer.data
			return Response(new_data, status=HTTP_200_OK)
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
	serializer_class = ArticleListSerializer
	queryset = Article.objects.all()
	permission_classes = [IsAuthenticated]
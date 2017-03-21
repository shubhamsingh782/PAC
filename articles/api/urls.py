from django.conf.urls import url
from .views import(
	 UserRegistrationAPIView,
	 UserLoginAPIView,
	 ArticleCreateAPIView,
	 ArticleListAPIView,
	 ArticleDetailAPIView
	 )
from rest_framework.authtoken import views
urlpatterns = [
		url(r'article_list/$',ArticleListAPIView.as_view(),name='article_list'),
		url(r'(?P<pk>\d+)/$',ArticleDetailAPIView.as_view(), name='detail'),
		url(r'create/$',ArticleCreateAPIView.as_view(), name='create'),
		url(r'^register/$',UserRegistrationAPIView.as_view(),name='register'),
		url(r'login/$',UserLoginAPIView.as_view(), name='login'),
		url(r'^auth/token/$', views.obtain_auth_token,name='auth_token'),
		]
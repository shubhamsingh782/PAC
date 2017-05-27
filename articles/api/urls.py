from django.conf.urls import url
from .views import(
	 UserRegistrationAPIView,
	 UserLoginAPIView,
	 ArticleCreateAPIView,
	 ArticleListAPIView,
	 ArticleDetailAPIView,
	 ArticleDeletAPIView,
	 APILogout,
	 AvailableUsername,
	 AvailableEmail,
	 ResetPasswordView,
	 SetPasswordView,
	 ChangePasswordView,
	 )
from rest_framework.authtoken import views
urlpatterns = [
		url(r'^article_list/$', ArticleListAPIView.as_view(), name='article_list'),
		url(r'^(?P<pk>\d+)/$', ArticleDetailAPIView.as_view(), name='detail'),
		url(r'^create/$', ArticleCreateAPIView.as_view(), name='create'),
		url(r'^register/$', UserRegistrationAPIView.as_view(), name='register'),
		url(r'^(?P<pk>\d+)/delete/$', ArticleDeletAPIView.as_view(), name='delete'),
		url(r'^login/$', UserLoginAPIView.as_view(), name='login'),
		url(r'^logout/$', APILogout.as_view(), name='logout'),
		#url(r'^auth/token/$', views.obtain_auth_token,name='auth_token'),

		url(r'^check_availability/$', AvailableUsername.as_view(), name='availability'),
		url(r'^change-password/$', ChangePasswordView.as_view(), name='change_password'),
		url(r'^check-email-availability/$', AvailableEmail.as_view(), name='availability'),
		url(r'^reset_password/$',ResetPasswordView.as_view(), name='reset_password'),
		url(r'^setpassword/$', SetPasswordView.as_view(), name='set_password'),
		]
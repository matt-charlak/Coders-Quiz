from django.conf.urls import url
from . import views

app_name = 'app'
urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^search/$', views.search, name='search'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^actualquiz/(\d+)$', views.actualquiz, name='actualquiz'),
    url(r'^user_profile/(\d+)$',
        views.user_profile, name='user_profile'),
]

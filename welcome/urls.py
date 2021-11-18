from django.urls import path

from welcome.api import hobby_api, hobbies_api
from . import views


app_name = "welcome"


urlpatterns = [
    path('', views.index, name="home"),
    path('api/hobby/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]

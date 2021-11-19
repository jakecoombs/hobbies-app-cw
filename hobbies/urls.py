from django.urls import path

from hobbies.api.hobby_api import hobby_api, hobbies_api
from . import views


app_name = "hobbies"


urlpatterns = [
    path('', views.index, name="home"),
    path('api/hobby/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]

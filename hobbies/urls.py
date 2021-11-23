from django.urls import path

from hobbies.api.hobby_api import hobby_api, hobbies_api
from hobbies.api.user_api import user_api, users_api, upload_image
from . import views


app_name = "hobbies"


urlpatterns = [
    path('', views.index, name="home"),
    path('api/hobby/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('api/user/<int:user_id>/', user_api, name='user_api'),
    path('api/users/', users_api, name='users_api'),
    path('api/uploadimage/', upload_image, name='upload_image'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]

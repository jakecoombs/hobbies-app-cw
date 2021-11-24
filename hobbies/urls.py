from django.urls import path

from hobbies.api.hobby_api import hobby_api, hobbies_api
from hobbies.api.user_api import active_user_api, user_api, users_api, upload_image, create_user_api
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('users', views.users, name="users"),
    path('api/hobbies/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('api/users/<int:user_id>/', user_api, name='user_api'),
    path('api/users/active/', active_user_api, name='active_user_api'),
    path('api/users/create/', create_user_api, name='create_user_api'),
    path('api/users/', users_api, name='users_api'),
    path('api/uploadimage/', upload_image, name='upload_image'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
]

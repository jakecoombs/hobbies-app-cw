from django.urls import path

from hobbies.api.hobby_api import hobby_api, hobbies_api
from hobbies.api.user_api import active_user_api, user_api, users_api, upload_image, create_user_api, send_friend_request_api, answer_friend_request_api, remove_friend_api
from . import views


urlpatterns = [
    path('', views.index, name="home"),
    path('users', views.users, name="users"),
    path('users/<int:user_id>/', views.user, name='user'),
    path('api/hobbies/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api'),
    path('api/users/<int:user_id>/', user_api, name='user_api'),
    path('api/users/active/', active_user_api, name='active_user_api'),
    path('api/users/create/', create_user_api, name='create_user_api'),
    path('api/users/', users_api, name='users_api'),
    path('api/uploadimage/', upload_image, name='upload_image'),
    path('api/sendfriendrequest/', send_friend_request_api, name='send_friend_request'),
    path('api/answerfriendrequest/', answer_friend_request_api, name='answer_friend_request'),
    path('api/removefriend/', remove_friend_api, name='remove_friend'),
    path('login/', views.login, name="login"),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.logout, name="logout"),
    path('hobbies/create/', views.create, name="create"),
    path('hobbies/create/api/hobbies/', views.create, name="create"),
    path('hobbies/<int:hobby_id>/', views.hobby, name='hobby'),
]

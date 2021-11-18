from django.urls import path
from . import views

from welcome.api import hobby_api, hobbies_api

urlpatterns = [
    path('', views.index, name="welcome-index"),

    path('api/hobby/<int:hobby_id>/', hobby_api, name='hobby_api'),
    path('api/hobbies/', hobbies_api, name='hobbies_api')
]

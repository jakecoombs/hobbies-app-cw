import json

from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404

from hobbies.models import Hobby, User


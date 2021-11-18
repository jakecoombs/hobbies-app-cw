import json

from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest

from welcome.models import Hobby, User


def hobby_api(request, hobby_id):
    if request.method == "PUT":
        print(f"Editing hobby {hobby_id}...")

    if request.method == "DELETE":
        print(f"Deleting hobby {hobby_id}...")

    else:
        return HttpResponseBadRequest("Invalid method")


def hobbies_api(request):
    if request.method == "POST":
        print(f"Creating new hobby...")

    if request.method == "GET":
        print(f"Retrieving all hobbies...")

    else:
        return HttpResponseBadRequest("Invalid method")

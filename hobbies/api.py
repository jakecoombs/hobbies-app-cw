import json

from django.http import JsonResponse, HttpRequest, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404

from hobbies.models import Hobby, User


def hobby_api(request, hobby_id):
    if request.method == "PUT":
        print(f"Editing hobby {hobby_id}...")

    if request.method == "DELETE":
        hobby = get_object_or_404(Hobby, id=hobby_id)
        hobby.users.clear()
        hobby.delete()
        return HttpResponse(200)

    return HttpResponseBadRequest("Invalid method")


def hobbies_api(request):
    if request.method == "POST":
        print(f"Creating new hobby...")
        return JsonResponse({})  # temp response

    if request.method == "GET":
        return JsonResponse({
            'hobbies': generate_hobbies_dict()
        })

    return HttpResponseBadRequest("Invalid method")


def generate_hobbies_dict():
    hobbies_dict = [hobby.to_dict() for hobby in Hobby.objects.all()]

    for hobby in hobbies_dict:
        hobby_object = Hobby.objects.get(id=hobby['id'])
        users_dict = [user.to_dict() for user in hobby_object.users.all()]
        hobby['users'] = [user.id for user in users_dict]

    return hobbies_dict

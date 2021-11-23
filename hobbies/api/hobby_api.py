import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.shortcuts import get_object_or_404

from hobbies.models import Hobby, User


@login_required
def hobby_api(request, hobby_id):
    if request.method == "PUT":
        editing_hobby_string = request.body.decode('utf8').replace("'", '"')
        editing_hobby_dict = json.loads(editing_hobby_string)
        hobby_to_change = Hobby.objects.get(id=hobby_id)
        hobby_to_change.name = editing_hobby_dict['name']
        hobby_to_change.description = editing_hobby_dict['description']
        hobby_to_change.users.clear()

        if "users" in editing_hobby_dict.keys():
            for userID in editing_hobby_dict['users']:
                user_to_add = User.objects.filter(id=userID).first()
                hobby_to_change.users.add(user_to_add)

        hobby_to_change.save()

        return HttpResponse(200)

    if request.method == "DELETE":
        hobby = get_object_or_404(Hobby, id=hobby_id)
        hobby.users.clear()
        hobby.delete()
        return HttpResponse(200)

    return HttpResponseBadRequest("Invalid method")


@login_required
def hobbies_api(request):
    if request.method == "POST":
        new_hobby_string = request.body.decode('utf8').replace("'", '"')
        new_hobby_dict = json.loads(new_hobby_string)
        new_hobby_object = Hobby(
            name=new_hobby_dict['name'],
            description=new_hobby_dict['description'])

        new_hobby_object.save()

        if "users" in new_hobby_dict.keys():
            for userID in new_hobby_dict['users']:
                user_to_add = User.objects.filter(id=userID).first()
                new_hobby_object.users.add(user_to_add)

        new_hobby_object.save()

        dict_to_return = new_hobby_object.to_dict()
        users_dict = [user.to_dict() for user in new_hobby_object.users.all()]
        dict_to_return['users'] = [user.id for user in users_dict]

        return JsonResponse({
            "hobby": dict_to_return
        })

    if request.method == "GET":
        return JsonResponse({
            'hobbies': generate_hobbies_dict()
        })

    return HttpResponseBadRequest("Invalid method")


@login_required
def generate_hobbies_dict():
    hobbies_dict = [hobby.to_dict() for hobby in Hobby.objects.all()]

    for hobby in hobbies_dict:
        hobby_object = Hobby.objects.get(id=hobby['id'])
        users_dict = [user.to_dict() for user in hobby_object.users.all()]
        hobby['users'] = [user.id for user in users_dict]

    return hobbies_dict

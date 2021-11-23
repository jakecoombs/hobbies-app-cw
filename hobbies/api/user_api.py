import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse, Http404
from django.shortcuts import get_object_or_404
from hobbies.models import Hobby, User
from .. import utils


@login_required
def user_api(request, user_id):
    if request.method == "PUT":
        editing_user_string = request.body.decode('utf8').replace("'", '"')
        editing_user_dict = json.loads(editing_user_string)
        user_to_change = User.objects.get(id=user_id)
        user_to_change.username = editing_user_dict['username']
        user_to_change.email = editing_user_dict['email']
        user_to_change.dob = editing_user_dict['dob']
        user_to_change.city = editing_user_dict['city']
        user_to_change.hobbies.clear()
        user_to_change.friends.clear()

        if "hobbies" in editing_user_dict.keys():
            for hobbyID in editing_user_dict['hobbies']:
                hobby_to_add = Hobby.objects.filter(id=hobbyID).first()
                user_to_change.hobbies.add(hobby_to_add)

        if "friends" in editing_user_dict.keys():
            for friendID in editing_user_dict['friend']:
                friend_to_add = User.objects.filter(id=friendID).first()
                user_to_change.friends.add(friend_to_add)

        user_to_change.save()

        return JsonResponse({
            "user": user_to_change.to_dict_with_hobbies_and_friends()
        })

    if request.method == "DELETE":
        user = get_object_or_404(User, id=user_id)
        user.friends.clear()
        user.hobbies.clear()
        user.delete()
        return HttpResponse(200)

    return HttpResponseBadRequest("Invalid method")


def users_api(request):
    if request.method == "POST":
        new_user_string = request.body.decode('utf8').replace("'", '"')
        new_user_dict = json.loads(new_user_string)
        new_user_object = User(
            username=new_user_dict['username'],
            email=new_user_dict['email'],
            dob=new_user_dict['dob'],
            city=new_user_dict['city'])

        new_user_object.save()

        if "hobbies" in new_user_dict.keys():
            for hobbyID in new_user_dict['hobbies']:
                hobby_to_add = Hobby.objects.filter(id=hobbyID).first()
                new_user_object.hobbies.add(hobby_to_add)

        if "friends" in new_user_dict.keys():
            for friendID in new_user_dict['friend']:
                friend_to_add = User.objects.filter(id=friendID).first()
                new_user_object.friends.add(friend_to_add)

        new_user_object.save()

        return JsonResponse({
            "user": new_user_object.to_dict_with_hobbies_and_friends()
        })

    if request.method == "GET":
        users = User.objects.all()

        # Check URL filters
        id_filter = request.GET.get('id', None)
        city_filter = request.GET.get('city', None)
        minimum_age_filter = request.GET.get('minimumAge', None)
        maximum_age_filter = request.GET.get('maximumAge', None)

        # Apply filters
        if id_filter:
            users = users.filter(id=id_filter)

        if city_filter:
            users = users.filter(city=city_filter)

        if minimum_age_filter:
            pivot_date = utils.calculate_pivot_date(minimum_age_filter)
            users = users.filter(dob__lte=pivot_date)

        if maximum_age_filter:
            pivot_date = utils.calculate_pivot_date(maximum_age_filter)
            users = users.filter(dob__gte=pivot_date)

        return JsonResponse({
            'users': [user.to_dict() for user in users],
            'total': len(users)
        })

    return HttpResponseBadRequest("Invalid method")


@login_required
def upload_image(request):
    user = request.user
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        user.image = image_file
        user.save()
        return JsonResponse({'imageUrl': user.image.url})
    else:
        raise Http404('Image file not received')

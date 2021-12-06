import json

from django.http import (Http404, HttpResponse, HttpResponseBadRequest,
                         JsonResponse)
from django.shortcuts import get_object_or_404
from hobbies.decorators import user_login_required
from hobbies.models import Hobby, User, FriendRequest

from .. import utils


@user_login_required()
def user_api(request, user_id):
    if request.method == "GET":
        user = User.objects.get(id=user_id)
        return JsonResponse({
            "user": user.to_dict_with_hobbies_and_friends()
        })

    if request.method == "PUT":
        editing_user_string = request.body.decode('utf8').replace("'", '"')
        editing_user_dict = json.loads(editing_user_string)
        user_to_change = User.objects.get(id=user_id)
        user_to_change.username = editing_user_dict['username']
        user_to_change.email = editing_user_dict['email']
        user_to_change.dob = editing_user_dict['dob']
        user_to_change.city = editing_user_dict['city']
        user_to_change.hobbies.clear()

        if "hobbies" in editing_user_dict.keys():
            for hobbyID in editing_user_dict['hobbies']:
                hobby_to_add = Hobby.objects.filter(id=hobbyID).first()
                user_to_change.hobbies.add(hobby_to_add)

        user_to_change.save()

        return JsonResponse({
            "user": user_to_change.to_dict_with_hobbies_and_friends()
        })

    if request.method == "DELETE":
        user = get_object_or_404(User, id=user_id)
        user.following.clear()
        user.hobbies.clear()
        user.delete()
        return HttpResponse(200)

    return HttpResponseBadRequest("Invalid method")


@user_login_required()
def active_user_api(request):
    if request.method == "GET":
        user = User.objects.get(id=request.user.id)
        return JsonResponse({
            "user": user.to_dict_with_hobbies_and_friends()
        })

    return HttpResponseBadRequest("Invalid method")


@user_login_required()
def users_api(request):
    if request.method == "GET":
        users = User.objects.all()

        # Check URL filters
        username_filter = request.GET.get('username', None)
        city_filter = request.GET.get('city', None)
        minimum_age_filter = request.GET.get('minAge', None)
        maximum_age_filter = request.GET.get('maxAge', None)

        # Apply filters
        if username_filter:
            users = users.filter(username=username_filter)

        if city_filter:
            users = users.filter(city=city_filter)

        if minimum_age_filter:
            pivot_date = utils.calculate_pivot_date(int(minimum_age_filter))
            users = users.filter(dob__lte=pivot_date)

        if maximum_age_filter:
            pivot_date = utils.calculate_pivot_date(int(maximum_age_filter))
            users = users.filter(dob__gte=pivot_date)

        return JsonResponse({
            'users': [user.to_dict_with_hobbies_and_friends() for user in users],
            'total': len(users)
        })

    return HttpResponseBadRequest("Invalid method")


def create_user_api(request):
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

        new_user_object.save()

        return JsonResponse({
            "user": new_user_object.to_dict_with_hobbies_and_friends()
        })
    return HttpResponseBadRequest("Invalid method")


@user_login_required()
def upload_image(request):
    user = request.user
    if 'img_file' in request.FILES:
        image_file = request.FILES['img_file']
        user.image = image_file
        user.save()
        return JsonResponse({'imageUrl': user.image.url})
    else:
        raise Http404('Image file not received')


@user_login_required()
def send_friend_request_api(request):
    if request.method == "POST":
        body_dict = json.loads(request.body.decode('utf8').replace("'", '"'))
        sender_id = request.user.id
        target_id = body_dict["targetId"]

        sender = User.objects.get(id=sender_id)
        target = User.objects.get(id=target_id)

        # don't create duplicate friend request
        if len(FriendRequest.objects.filter(sender_user=sender, target_user=target)) > 0:
            return HttpResponse("Cannot create duplicate friend request", status=500)

        friend_request = FriendRequest(sender_user=sender, target_user=target)
        friend_request.save()

        return JsonResponse({
            'sender': sender.to_dict_with_hobbies_and_friends(),
            'target': target.to_dict_with_hobbies_and_friends()
        })

    return HttpResponseBadRequest("Invalid method")


@user_login_required()
def answer_friend_request_api(request):
    if request.method == "POST":
        body_dict = json.loads(request.body.decode('utf8').replace("'", '"'))
        target_id = request.user.id
        sender_id = body_dict["senderId"]
        approve = body_dict["approve"]

        sender = User.objects.get(id=sender_id)
        target = User.objects.get(id=target_id)

        # The target of the response sent the request originally
        friend_requests = FriendRequest.objects.filter(sender_user=sender,
                                                       target_user=target)

        if len(friend_requests) < 1:
            return HttpResponse("No such friend request exists", status=500)

        friend_request = friend_requests.first()

        if approve:
            target.following.add(sender)
            target.save()

        friend_request.delete()

        return JsonResponse({
            'sender': sender.to_dict_with_hobbies_and_friends(),
            'target': target.to_dict_with_hobbies_and_friends()
        })

    return HttpResponseBadRequest("Invalid method")


@user_login_required()
def remove_friend_api(request):
    if request.method == "POST":
        body_dict = json.loads(request.body.decode('utf8').replace("'", '"'))
        sender_id = request.user.id
        target_id = body_dict["targetId"]

        sender = User.objects.get(id=sender_id)
        target = User.objects.get(id=target_id)

        sender.following.remove(target)
        sender.save()

        return JsonResponse({
            'sender': sender.to_dict_with_hobbies_and_friends(),
            'target': target.to_dict_with_hobbies_and_friends()
        })

    return HttpResponseBadRequest("Invalid method")

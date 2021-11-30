from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

DEFAULT_USER_PROFILE_IMAGE = 'https://media.istockphoto.com/vectors/default-profile-picture-avatar-photo-placeholder-vector-illustration-vector-id1223671392?k=20&m=1223671392&s=612x612&w=0&h=lGpj2vWAI3WUT1JeJWm1PRoHT3V15_1pdcTn2szdwQ0='


class FriendRequest(models.Model):
    sender_user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="sender")
    target_user = models.OneToOneField("User", on_delete=models.CASCADE, related_name="target")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender_user', 'target_user'], name="unique_friend_request")
        ]

    def to_dict(self):
        return {
            "sender_id": self.sender_user.id,
            "target_id": self.target_user.id
        }

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=50)
    dob = models.DateField()

    city = models.CharField(max_length=20, null=True)
    image = models.ImageField(upload_to="profile_pictures", null=True)

    following = models.ManyToManyField(
        to="self",
        blank=True,
        symmetrical=True,
        related_name="friends",
    )

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'dob': self.dob,
            'city': self.city if self.city else None,
            'image': self.image.url if self.image else DEFAULT_USER_PROFILE_IMAGE
        }

    def to_dict_with_hobbies_and_friends(self):
        user_dict = self.to_dict()

        hobbies_dict = [hobby.to_dict()
                        for hobby in self.hobbies.all()]
        user_dict['hobbies'] = {
            'hobbies': [
                hobby["id"] for hobby in hobbies_dict],
            'total': len(hobbies_dict)
        }

        friends_dict = [friend.to_dict()
                        for friend in self.following.all()]
        user_dict['friends'] = {
            'friends': [
                friend["id"] for friend in friends_dict],
            'total': len(friends_dict)
        }

        outgoing_friend_requests = FriendRequest.objects.filter(sender_user=self)
        user_dict["outgoingFriendRequests"] = {
            "outgoingFriendRequests": [
                request.id for request in outgoing_friend_requests
            ],
            "total": len(outgoing_friend_requests)
        }

        incoming_friend_requests = FriendRequest.objects.filter(target_user=self)
        user_dict["incomingFriendRequests"] = {
            "incomingFriendRequests": [
                request.id for request in incoming_friend_requests
            ],
            "total": len(incoming_friend_requests)
        }

        return user_dict


class Hobby(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=300)
    users = models.ManyToManyField(User, related_name="hobbies")

    def __str__(self):
        return f"{self.name}, {self.description}"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'api': reverse('hobby-api', kwargs={'hobby_id': self.id})
        }

    def to_dict_with_users(self):
        hobby_dict = self.to_dict()
        users_dict = [user.to_dict() for user in self.users.all()]
        hobby_dict['users'] = {
            'ids': [user["id"] for user in users_dict],
            'length': len(users_dict)
        }
        return hobby_dict

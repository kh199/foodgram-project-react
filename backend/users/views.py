from djoser.views import UserViewSet
from django.contrib.auth import get_user_model
from .models import Follow
from api.serializers import SubscriptionsSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework import status

User = get_user_model()


class CustomUserViewSet(UserViewSet):

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        follow = Follow.objects.filter(user=request.user)
        serializer = SubscriptionsSerializer(
            follow, many=True,
            context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        follow = Follow.objects.create(user=request.user, author=author)
        serializer = SubscriptionsSerializer(
            follow, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        author = get_object_or_404(User, id=id)
        follow = get_object_or_404(Follow, user=request.user, author=author)
        follow.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

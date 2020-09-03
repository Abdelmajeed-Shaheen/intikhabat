from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import VoterSerializer,LoginSerializer
from users_management.models import UserProfile,Voter
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User

class UserProfileViewSet(viewsets.ViewSet):
    """Handles creating, reading and updating profiles."""

    # permission_classes=[IsAuthenticated]
   
    def retrieve(self, request,pk=None):
        user=User.objects.get(pk=pk)
        user = UserProfile.objects.get(user=user)
        if hasattr(user,"voter"):
            user=Voter.objects.get(profile=user)
            serializer = VoterSerializer(user)
        return Response(serializer.data)

class GetCredsViewSet(APIView):

    permission_classes = (IsAuthenticated,)        

    def get(self, request):
        user=request.user.id
        content = {'id': user,'username':request.user.username}
        return Response(content)
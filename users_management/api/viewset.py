from rest_framework import viewsets
from rest_framework.views import APIView
from .serializers import (
                          VoterSerializer,LoginSerializer,
                          CandidateProfileSerializer,CampaignAdminProfileSerializer,
                          ComitteeMemberSerializer
                          )
from users_management.models import (
                                     UserProfile,Voter,
                                     Candidate,CampaignAdminstrator,
                                     ComitteeMember
                                     )

from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken

from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth.models import User

class UserProfileViewSet(viewsets.ViewSet):
    """ Handles retrieving  profiles. """

    permission_classes=(IsAuthenticated,)
   
    def retrieve(self, request,pk=None):
        user=User.objects.get(pk=pk)
        user = UserProfile.objects.get(user=user)
        if hasattr(user,"voter"):
            user=Voter.objects.get(profile=user)
            serializer = VoterSerializer(user)
        elif hasattr(user,"candidate"):
            user=Candidate.objects.get(profile=user)
            serializer=CandidateProfileSerializer(user)

        elif hasattr(user,"campaignadminstrator"):
            user=CampaignAdminstrator.objects.get(profile=user)
            serializer=CampaignAdminProfileSerializer(user)
        elif hasattr(user,"comitteemember"):
            user=ComitteeMember.objects.get(profile=user)
            serializer=ComitteeMemberSerializer(user)
        
        return Response(serializer.data)



class GetCredsViewSet(APIView):


    allowed_methods=['post']

    def get(self, request):
        user=request.user.id
        content = {'id': user,'username':request.user.username}
        return Response(content)

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class LoginViewSet(viewsets.ViewSet):
    """ Check username and password and returns an auth token"""

    serializer_class = AuthTokenSerializer

    def create(self, request):
        try:
            
            user = User.objects.get(id=request.user.id)
            token = get_tokens_for_user(user)
            return Response({
                            'status':True,'message':'Login successful',
                            'data':{
                                    'token': token["access"],
                                    'refresh':token["refresh"],
                                    'id': user.id, 
                                    'first_name': user.first_name, 
                                    'last_name': user.last_name, 
                                    'email': user.email
                                    
                                    }
                                })
        except:
            return Response({'status':False,'message':'Invalid Username/Password.'})


# class ObtainAuthTokenID(ObtainAuthToken):
#     """ Auth token generation """
#     def post(self, request, *args, **kwargs):
#         try:
            
#             user = User.objects.get(id=request.user.id)
#             token = get_tokens_for_user(user)
#             return Response({
#                             'status':True,'message':'Login successful',
#                             'data':{
#                                     'token': token["access"],
#                                     'refresh':token["refresh"],
#                                     'id': user.id, 
#                                     'first_name': user.first_name, 
#                                     'last_name': user.last_name, 
#                                     'email': user.email
                                    
#                                     }
#                                 })
#         except:
#             return Response({'status':False,'message':'Invalid Username/Password.'})

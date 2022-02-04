from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from uritemplate import partial
from .serializers import UserSerializer

# Create your views here.

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user(request):
    user = User.objects.get(username=request.user)
    serializer = UserSerializer(user)
    return Response(status=200, data=serializer.data)

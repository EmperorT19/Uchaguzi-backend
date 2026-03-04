from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import VoterRegistrationSerializer


@api_view(["GET"])
def index(request):
    return Response("Hello Timo")


@api_view(["POST"])
def signup(request):
    serializer = VoterRegistrationSerializer(data=request.data)

    if serializer.is_valid():
        voter = serializer.save()
        return Response(
            {
                "message": "Registration successful",
                "voter_code": voter.voter_code,
            },
            status=status.HTTP_201_CREATED,
        )

    return Response(
        {"errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


    

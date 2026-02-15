from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.
from.models import *
from django.db.utils import IntegrityError
@api_view(['GET'])
def index (request): 
        return Response("Hello Timo")
    
@api_view(['POST'])
def signup (request):
    if request.method == "POST":  
            print(request.data)
            try:
                user = Voter.objects.create(
                    full_name=request.data.get("fullName").strip(),
                    phone_number=request.data.get("phone").strip(),
                    constituency=request.data.get("constituency").strip(),
                    county=request.data.get("county").strip(),
                    ward=request.data.get("ward").strip(),
                    id_number=request.data.get("idNumber"),
                    email = request.data.get("email")
                )
        
                user.save()
                return Response({"message":"Registration successful"}, status=200)
            except IntegrityError:
                return Response({"message":"User already exists"}, status=401)
    return Response({"message":"signup"}, status=200)


    

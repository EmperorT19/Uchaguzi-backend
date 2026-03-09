import uuid
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
from.models import *
from django.db.utils import IntegrityError
from django.views.decorators.csrf import csrf_exempt

@api_view(['GET'])
def index (request): 
        return Response("Hello Timo")
    
@api_view(['POST'])
@csrf_exempt
def signup (request):
    if request.method == "POST":  
        print(request.data)
        generated_uuid = uuid.uuid4()
        try:
            user = Voter.objects.create(
                full_name=request.data.get("full_name").strip(),
                phone_number=request.data.get("phone").strip(),
                constituency=request.data.get("constituency"),
                county=request.data.get("county"),
                ward=request.data.get("ward"),
                id_number=request.data.get("id_number"),
                email = request.data.get("email"),
                voter_code=generated_uuid,
                password_hash=generated_uuid
            )
    
            user.save()
            send_mail(
                    subject='Your Uchaguzi Voter Code',
                    message=f'Hello {user.full_name},\n\nYour voter code is: {generated_uuid}\n\nUse this code along with your ID number to log in and vote.\n\nuChaguzi Electoral System',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email, 'muokijr@gmail.com'],
                    fail_silently=False,
                )
            return Response({"message":"Registration successful", "voter_code": str(generated_uuid)}, status=200)
        except IntegrityError:
            return Response({"message":"User already exists"}, status=200)
    return Response({"message":"signup"}, status=200)


# @api_view(["POST"])
# def login(request):
#     if request.method == "POST":
#         print(request.data)
#         return Response({"message":"login"}, status=200)

@api_view(["POST"])
def login(request):
    id_number = request.data.get("id_number", "").strip()
    voter_code = request.data.get("voter_code", "").strip()

    if not id_number or not voter_code:
        return Response({"message": "ID number and voter code are required"}, status=400)

    try:
        voter = Voter.objects.get(id_number=id_number, voter_code=voter_code)
    except Voter.DoesNotExist:
        return Response({"message": "Invalid credentials"}, status=401)

    voted_seats = Vote.objects.filter(voter=voter).values_list('seat__seat_type', flat=True)

    return Response({
        "message": "Login successful",
        "user": {
            "id": voter.id,
            "full_name": voter.full_name,
            "voter_code": str(voter.voter_code),
            "id_number": voter.id_number,
            "county": voter.county,
            "constituency": voter.constituency,
            "ward": voter.ward,
            "has_voted": list(voted_seats)
        }
    }, status=200)
    
#vote api

@api_view(["POST"])
def cast_vote(request):
    print("DATA RECEIVED:", request.data)
    try:
        voter_id = int(request.data.get("voter_id"))
        seat_id = int(request.data.get("seat_id"))
        candidate_id = int(request.data.get("candidate_id"))
        print(f"IDs: voter={voter_id}, seat={seat_id}, candidate={candidate_id}")
    except (TypeError, ValueError) as e:
        print("CONVERSION ERROR:", e)
        return Response({"message": "Invalid ID format"}, status=400)

    try:
        voter = Voter.objects.get(id=voter_id)
        print("Voter found:", voter)
    except Voter.DoesNotExist:
        print("Voter NOT found")
        return Response({"message": "Voter not found"}, status=404)

    try:
        seat = Seat.objects.get(id=seat_id)
        print("Seat found:", seat)
    except Seat.DoesNotExist:
        print("Seat NOT found")
        return Response({"message": "Seat not found"}, status=404)

    try:
        candidate = Candidate.objects.get(id=candidate_id)
        print("Candidate found:", candidate)
    except Candidate.DoesNotExist:
        print("Candidate NOT found")
        return Response({"message": "Candidate not found"}, status=404)

    try:
        Vote.objects.create(voter=voter, seat=seat, candidate=candidate)
        return Response({"message": "Vote cast successfully"}, status=200)
    except IntegrityError:
        return Response({"message": "You have already voted for this seat"}, status=400)
    
@api_view(["GET"])
def get_candidates(request):
    county = request.GET.get("county")
    constituency = request.GET.get("constituency")
    ward = request.GET.get("ward")

    seats = Seat.objects.all()
    result = []

    for seat in seats:
        if seat.level == 'National':
            candidates = Candidate.objects.filter(seat=seat)
        elif seat.level == 'County':
            candidates = Candidate.objects.filter(seat=seat, seat__county=county)
        elif seat.level == 'Constituency':
            candidates = Candidate.objects.filter(seat=seat, seat__constituency=constituency)
        elif seat.level == 'Ward':
            candidates = Candidate.objects.filter(seat=seat, seat__ward=ward)
        else:
            candidates = []

        result.append({
            "seat_id": seat.id,
            "seat_type": seat.seat_type,
            "seat_name": seat.name,
            "candidates": [{"id": c.id, "full_name": c.full_name, "party": c.party} for c in candidates]
        })

    return Response(result, status=200)


@api_view(["GET"])
def get_results(request):
    seat_type = request.GET.get("seat_type")
    seats = Seat.objects.filter(seat_type=seat_type) if seat_type else Seat.objects.all()
    result = []

    for seat in seats:
        candidates = Candidate.objects.filter(seat=seat)
        result.append({
            "seat_id": seat.id,
            "seat_type": seat.seat_type,
            "seat_name": seat.name,
            "results": [
                {
                    "candidate_id": c.id,
                    "full_name": c.full_name,
                    "party": c.party,
                    "votes": Vote.objects.filter(candidate=c).count()
                }
                for c in candidates
            ]
        })

    return Response(result, status=200)


@api_view(["GET"])
def voter_status(request):
    voter_id = request.GET.get("voter_id")
    if not voter_id:
        return Response({"message": "voter_id required"}, status=400)

    try:
        voter = Voter.objects.get(id=voter_id)
    except Voter.DoesNotExist:
        return Response({"message": "Voter not found"}, status=404)

    voted_seats = Vote.objects.filter(voter=voter).values_list('seat__seat_type', flat=True)
    return Response({"has_voted": list(voted_seats)}, status=200)
    
    
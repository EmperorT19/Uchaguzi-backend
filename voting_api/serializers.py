import string
import secrets

from rest_framework import serializers
from django.contrib.auth.hashers import make_password, check_password

from .models import Voter, Seat, Candidate, Vote


def generate_voter_code(length=8):
    """Generate a unique alphanumeric voter code."""
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if not Voter.objects.filter(voter_code=code).exists():
            return code


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------
class VoterRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Voter
        fields = [
            "full_name",
            "id_number",
            "phone_number",
            "email",
            "county",
            "constituency",
            "ward",
            "password",
        ]

    def create(self, validated_data):
        raw_password = validated_data.pop("password")
        validated_data["voter_code"] = generate_voter_code()
        validated_data["password_hash"] = make_password(raw_password)
        return super().create(validated_data)


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------
class VoterLoginSerializer(serializers.Serializer):
    id_number = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        id_number = attrs["id_number"].strip()
        password = attrs["password"]

        try:
            voter = Voter.objects.get(id_number=id_number)
        except Voter.DoesNotExist:
            raise serializers.ValidationError("Invalid credentials.")

        if not check_password(password, voter.password_hash):
            raise serializers.ValidationError("Invalid credentials.")

        attrs["voter"] = voter
        return attrs


# ---------------------------------------------------------------------------
# Electoral data
# ---------------------------------------------------------------------------
class SeatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Seat
        fields = ["id", "seat_type", "name", "level", "icon", "county", "constituency", "ward"]


class CandidateSerializer(serializers.ModelSerializer):
    seat_type = serializers.CharField(source="seat.seat_type", read_only=True)

    class Meta:
        model = Candidate
        fields = ["id", "seat", "seat_type", "full_name", "party", "photo_url", "manifesto"]


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ["id", "voter", "seat", "candidate", "voted_at"]
        read_only_fields = ["voter", "voted_at"]


class VoteResultSerializer(serializers.Serializer):
    """Read-only serializer for aggregated results."""
    candidate_id = serializers.IntegerField()
    candidate_name = serializers.CharField()
    party = serializers.CharField(allow_null=True)
    seat_id = serializers.IntegerField()
    seat_type = serializers.CharField()
    seat_name = serializers.CharField()
    vote_count = serializers.IntegerField()

import string
import secrets

from rest_framework import serializers
from django.contrib.auth.hashers import make_password

from .models import Voter


def generate_voter_code(length=8):
    """Generate a unique alphanumeric voter code."""
    alphabet = string.ascii_uppercase + string.digits
    while True:
        code = "".join(secrets.choice(alphabet) for _ in range(length))
        if not Voter.objects.filter(voter_code=code).exists():
            return code


class VoterRegistrationSerializer(serializers.ModelSerializer):
    # Accept a plain-text password from the client; write-only so it never
    # appears in responses.
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
        # Pop the plain-text password — it doesn't map to a model field.
        raw_password = validated_data.pop("password")

        # Auto-generate a unique voter code.
        validated_data["voter_code"] = generate_voter_code()

        # Hash the password before persisting.
        validated_data["password_hash"] = make_password(raw_password)

        return super().create(validated_data)

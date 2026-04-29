
# from django.db import models


# # =========================
# # Voter Model
# # =========================
# class Voter(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     voter_code = models.CharField(max_length=50, unique=True)
#     full_name = models.CharField(max_length=200)
#     id_number = models.CharField(max_length=20, unique=True)
#     phone_number = models.CharField(max_length=15, blank=True, null=True)
#     email = models.EmailField(max_length=100, blank=True, null=True)
#     county = models.IntegerField()
#     constituency = models.IntegerField()
#     ward = models.IntegerField()
#     password_hash = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['voter_code'], name='idx_voter_code'),
#             models.Index(fields=['id_number'], name='idx_id_number'),
#         ]

#     def __str__(self):
#         return self.full_name


# # =========================
# # Seat Model
# # =========================
# class Seat(models.Model):
#     SEAT_TYPES = [
#         ('president', 'President'),
#         ('governor', 'Governor'),
#         ('senator', 'Senator'),
#         ('mp', 'MP'),
#         ('woman_rep', 'Woman Rep'),
#         ('mca', 'MCA'),
#     ]

#     LEVELS = [
#         ('National', 'National'),
#         ('County', 'County'),
#         ('Constituency', 'Constituency'),
#         ('Ward', 'Ward'),
#     ]

#     id = models.BigAutoField(primary_key=True)
#     seat_type = models.CharField(max_length=20, choices=SEAT_TYPES)
#     name = models.CharField(max_length=200)
#     level = models.CharField(max_length=20, choices=LEVELS)
#     icon = models.CharField(max_length=10, blank=True, null=True)
#     county = models.CharField(max_length=100, blank=True, null=True)
#     constituency = models.CharField(max_length=100, blank=True, null=True)
#     ward = models.CharField(max_length=100, blank=True, null=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['seat_type', 'county', 'constituency', 'ward'],
#                 name='unique_seat'
#             )
#         ]

#     def __str__(self):
#         return f"{self.name} ({self.seat_type})"


# # =========================
# # Candidate Model
# # =========================
# class Candidate(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     seat = models.ForeignKey(
#         Seat,
#         on_delete=models.CASCADE,
#         related_name='candidates'
#     )
#     full_name = models.CharField(max_length=200)
#     party = models.CharField(max_length=100, blank=True, null=True)
#     photo_url = models.URLField(max_length=500, blank=True, null=True)
#     manifesto = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         indexes = [
#             models.Index(fields=['seat'], name='idx_seat_id'),
#         ]

#     def __str__(self):
#         return self.full_name


# # =========================
# # Vote Model
# # =========================
# class Vote(models.Model):
#     id = models.BigAutoField(primary_key=True)
#     voter = models.ForeignKey(
#         Voter,
#         on_delete=models.CASCADE,
#         related_name='votes'
#     )
#     seat = models.ForeignKey(
#         Seat,
#         on_delete=models.CASCADE,
#         related_name='votes'
#     )
#     candidate = models.ForeignKey(
#         Candidate,
#         on_delete=models.CASCADE,
#         related_name='votes'
#     )
#     voted_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=['voter', 'seat'],
#                 name='one_vote_per_seat'
#             )
#         ]
#         indexes = [
#             models.Index(fields=['voter'], name='idx_user_votes'),
#             models.Index(fields=['seat'], name='idx_seat_votes'),
#             models.Index(fields=['candidate'], name='idx_candidate_votes'),
#         ]

#     def __str__(self):
#         return f"Vote by {self.voter} for {self.candidate}"

from django.db import models


# =========================
# Voter Model: Stores localized regional data to ensure users see 
# their correct County/Constituency/Ward candidates.
# =========================
class Voter(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    county = models.IntegerField()
    constituency = models.IntegerField()
    ward = models.IntegerField()
    password_hash = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['voter_code'], name='idx_voter_code'),
            models.Index(fields=['id_number'], name='idx_id_number'),
        ]

    def __str__(self):
        return self.full_name


# =========================
# Seat Model: Defines levels (National, County, Ward) and 
# types (President, Governor, MCA, etc.)
# =========================
class Seat(models.Model):
    SEAT_TYPES = [
        ('president', 'President'),
        ('governor', 'Governor'),
        ('senator', 'Senator'),
        ('mp', 'MP'),
        ('woman_rep', 'Woman Rep'),
        ('mca', 'MCA'),
    ]

    LEVELS = [
        ('National', 'National'),
        ('County', 'County'),
        ('Constituency', 'Constituency'),
        ('Ward', 'Ward'),
    ]

    id = models.BigAutoField(primary_key=True)
    seat_type = models.CharField(max_length=20, choices=SEAT_TYPES)
    name = models.CharField(max_length=200)
    level = models.CharField(max_length=20, choices=LEVELS)
    icon = models.CharField(max_length=10, blank=True, null=True)
    
    # -------------------------------------------------------------
    # FIXED: Changed from CharField to IntegerField to match Voter
    # -------------------------------------------------------------
    county = models.IntegerField(blank=True, null=True)
    constituency = models.IntegerField(blank=True, null=True)
    ward = models.IntegerField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['seat_type', 'county', 'constituency', 'ward'],
                name='unique_seat'
            )
        ]

    def __str__(self):
        return f"{self.name} ({self.seat_type})"


# =========================
# Candidate Model: Linked to a Seat and contains biographical data 
# used for AI summaries and ballots.
# =========================
class Candidate(models.Model):
    id = models.BigAutoField(primary_key=True)
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='candidates'
    )
    full_name = models.CharField(max_length=200)
    party = models.CharField(max_length=100, blank=True, null=True)
    photo_url = models.URLField(max_length=500, blank=True, null=True)
    manifesto = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['seat'], name='idx_seat_id'),
        ]

    def __str__(self):
        return self.full_name


# =========================
# Vote Model: Records every cast ballot with a timestamp 
# for transparent, real-time election tracking.
# =========================
class Vote(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter = models.ForeignKey(
        Voter,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    seat = models.ForeignKey(
        Seat,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    candidate = models.ForeignKey(
        Candidate,
        on_delete=models.CASCADE,
        related_name='votes'
    )
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['voter', 'seat'],
                name='one_vote_per_seat'
            )
        ]
        indexes = [
            models.Index(fields=['voter'], name='idx_user_votes'),
            models.Index(fields=['seat'], name='idx_seat_votes'),
            models.Index(fields=['candidate'], name='idx_candidate_votes'),
        ]

    def __str__(self):
        return f"Vote by {self.voter} for {self.candidate}"

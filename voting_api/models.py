# from django.db import models

# from sqlalchemy import (
#     Column,
#     Integer,
#     String,
#     Text,
#     Enum,
#     ForeignKey,
#     TIMESTAMP,
#     UniqueConstraint,
#     Index
# )
# from sqlalchemy.orm import relationship, declarative_base
# from sqlalchemy.sql import func

# Base = declarative_base()


# # =========================
# # Users Model
# # =========================
# class Voter(models.Model):
 

#     id = models.BigAutoField(primary_key=True)
#     voter_code = models.CharField(max_length=200)
#     full_name = models.CharField(max_length=200)
#     id_number = models.CharField(max_length=200)
#     phone_number = models.CharField(max_length=200)
#     email = models.CharField(max_length=200)
#     county = models.CharField(max_length=200)
#     constituency = models.CharField(max_length=200)
#     ward = models.CharField(max_length=200)
#     password_hash = models.CharField(max_length=200)
#     created_at = models.DateTimeField()

#     votes = relationship("Vote", back_populates="user", cascade="all, delete")

#     __table_args__ = (
#         Index('idx_voter_code', 'voter_code'),
#         Index('idx_id_number', 'id_number'),
#     )

#     def __repr__(self):
#         return f"<User(id={self.id}, voter_code='{self.voter_code}', full_name='{self.full_name}')>"


# # =========================
# # Seats Model
# # =========================
# class Seat(models.Model):
#     __tablename__ = 'seats'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     seat_type = Column(
#         Enum('president', 'governor', 'senator', 'mp', 'woman_rep', 'mca'),
#         nullable=False
#     )
#     name = Column(String(200), nullable=False)
#     level = Column(
#         Enum('National', 'County', 'Constituency', 'Ward'),
#         nullable=False
#     )
#     icon = Column(String(10))
#     county = Column(String(100))
#     constituency = Column(String(100))
#     ward = Column(String(100))

#     candidates = relationship("Candidate", back_populates="seat", cascade="all, delete")
#     votes = relationship("Vote", back_populates="seat", cascade="all, delete")

#     __table_args__ = (
#         UniqueConstraint(
#             'seat_type', 'county', 'constituency', 'ward',
#             name='unique_seat'
#         ),
#     )

#     def __repr__(self):
#         return f"<Seat(id={self.id}, seat_type='{self.seat_type}', name='{self.name}')>"


# # =========================
# # Candidates Model
# # =========================
# class Candidate(models.Model):
#     __tablename__ = 'candidates'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     seat_id = Column(Integer, ForeignKey('seats.id', ondelete='CASCADE'), nullable=False)
#     full_name = Column(String(200), nullable=False)
#     party = Column(String(100))
#     photo_url = Column(String(500))
#     manifesto = Column(Text)
#     created_at = Column(TIMESTAMP, server_default=func.current_timestamp())

#     seat = relationship("Seat", back_populates="candidates")
#     votes = relationship("Vote", back_populates="candidate", cascade="all, delete")

#     __table_args__ = (
#         Index('idx_seat_id', 'seat_id'),
#     )

#     def __repr__(self):
#         return f"<Candidate(id={self.id}, full_name='{self.full_name}', party='{self.party}')>"


# # =========================
# # Votes Model
# # =========================
# class Vote(models.Model):
#     __tablename__ = 'votes'

#     id = Column(Integer, primary_key=True, autoincrement=True)
#     user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
#     seat_id = Column(Integer, ForeignKey('seats.id', ondelete='CASCADE'), nullable=False)
#     candidate_id = Column(Integer, ForeignKey('candidates.id', ondelete='CASCADE'), nullable=False)
#     voted_at = Column(TIMESTAMP, server_default=func.current_timestamp())

#     user = relationship("User", back_populates="votes")
#     seat = relationship("Seat", back_populates="votes")
#     candidate = relationship("Candidate", back_populates="votes")

#     __table_args__ = (
#         UniqueConstraint('user_id', 'seat_id', name='one_vote_per_seat'),
#         Index('idx_user_votes', 'user_id'),
#         Index('idx_seat_votes', 'seat_id'),
#         Index('idx_candidate_votes', 'candidate_id'),
#     )

#     def __repr__(self):
#         return (
#             f"<Vote(id={self.id}, user_id={self.user_id}, "
#             f"seat_id={self.seat_id}, candidate_id={self.candidate_id})>"
#         )


# # # Create your models here.
from django.db import models


# =========================
# Voter Model
# =========================
class Voter(models.Model):
    id = models.BigAutoField(primary_key=True)
    voter_code = models.CharField(max_length=50, unique=True)
    full_name = models.CharField(max_length=200)
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100)
    constituency = models.CharField(max_length=100)
    ward = models.CharField(max_length=100)
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
# Seat Model
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
    county = models.CharField(max_length=100, blank=True, null=True)
    constituency = models.CharField(max_length=100, blank=True, null=True)
    ward = models.CharField(max_length=100, blank=True, null=True)

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
# Candidate Model
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
# Vote Model
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

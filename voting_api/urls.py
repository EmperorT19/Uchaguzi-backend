from django.urls import path

from .views import (
    index,
    signup,
    login,
    seats_for_voter,
    candidates_for_seat,
    cast_vote,
    vote_results,
    voter_votes,
)

urlpatterns = [
    # Public
    path('timo/', index),
    path('register/', signup),
    path('voters/login/', login, name='voter-login'),

    # Authenticated
    path('seats/', seats_for_voter, name='seats-for-voter'),
    path('seats/<int:seat_id>/candidates/', candidates_for_seat, name='candidates-for-seat'),
    path('votes/', cast_vote, name='cast-vote'),
    path('votes/results/', vote_results, name='vote-results'),
    path('votes/mine/', voter_votes, name='voter-votes'),
]
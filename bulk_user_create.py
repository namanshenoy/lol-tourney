import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from webapp.models import UserProfile
from random import randint
import random
import string

def random_mmr():
    rank = randint(0, 10000)
    if(rank <= 3):
        return int(randint(2900, 3200))
    elif(rank <= 8):
        return int(randint(2550, 2899))
    elif(rank <= 168):
        return int(randint(2200, 2549))
    elif(rank <= 803):
        return int(randint(1850, 2199))
    elif(rank <= 2403):
        return int(randint(1500, 1849))
    elif(rank <= 6144):
        return int(randint(1150, 1499))
    elif(rank <= 10000):
        return int(randint(900, 1145))


User = get_user_model()

#  Update the users in this list.
#  Each tuple represents the username, password, and email of a user.
users = [
    ('user_1', 'Naman123', 'user_1@example.com'),
    ('user_2', 'Naman123', 'user_2@example.com'),
    ('user_3', 'Naman123', 'user_3@example.com'),
    ('user_37', 'Naman123', 'user_4@example.com'),
    ('user_4', 'Naman123', 'user_5@example.com'),
    ('user_5', 'Naman123', 'user_6@example.com'),
    ('user_6', 'Naman123', 'user_7@example.com'),
    ('user_7', 'Naman123', 'user_8@example.com'),
    ('user_8', 'Naman123', 'user_9@example.com'),
    ('user_9', 'Naman123', 'user_10@example.com'),
    ('user_10', 'Naman123', 'user_11@example.com'),
    ('user_11', 'Naman123', 'user_12@example.com'),
    ('user_12', 'Naman123', 'user_13@example.com'),
    ('user_13', 'Naman123', 'user_14@example.com'),
    ('user_14', 'Naman123', 'user_15@example.com'),
    ('user_15', 'Naman123', 'user_16@example.com'),
    ('user_16', 'Naman123', 'user_17@example.com'),
    ('user_17', 'Naman123', 'user_18@example.com'),
    ('user_18', 'Naman123', 'user_19@example.com'),
    ('user_19', 'Naman123', 'user_20@example.com'),
    ('user_20', 'Naman123', 'user_21@example.com'),
    ('user_21', 'Naman123', 'user_22@example.com'),
    ('user_22', 'Naman123', 'user_23@example.com'),
    ('user_23', 'Naman123', 'user_24@example.com'),
    ('user_24', 'Naman123', 'user_25@example.com'),
    ('user_25', 'Naman123', 'user_26@example.com'),
    ('user_26', 'Naman123', 'user_27@example.com'),
    ('user_27', 'Naman123', 'user_28@example.com'),
    ('user_28', 'Naman123', 'user_29@example.com'),
    ('user_29', 'Naman123', 'user_30@example.com'),
    ('user_30', 'Naman123', 'user_31@example.com'),
    ('user_31', 'Naman123', 'user_32@example.com'),
    ('user_32', 'Naman123', 'user_33@example.com'),
    ('user_33', 'Naman123', 'user_34@example.com'),
    ('user_34', 'Naman123', 'user_35@example.com'),
    ('user_35', 'Naman123', 'user_36@example.com'),
    ('user_36', 'Naman123', 'user_37@example.com'),
]


for username, password, email in users:
    try:
        print 'Creating user {0}.'.format(username)
        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.save()
        up = UserProfile.objects.create(user=User.objects.get(username=username),lol_mmr=random_mmr(), lol_summoner_name=''.join(random.choice(string.lowercase) for i in range(10)), primary_role=int(randint(1, 5)), secondary_role=int(randint(1, 5)))
        up.save()
        assert authenticate(username=username, password=password)
        print 'User {0} successfully created.'.format(username)

    except:
        print 'There was a problem creating the user: {0}.  Error: {1}.' \
            .format(username, sys.exc_info()[1])

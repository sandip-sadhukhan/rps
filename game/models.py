from django.db import models
from .utils import get_id, send_message
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

channel_layer = get_channel_layer()


class Room(models.Model):
    id = models.CharField(
        primary_key=True,
        default=get_id,
        editable=False,
        max_length=6
    )
    currentRound = models.IntegerField(
        null=True, blank=True
    )
    # users
    user1 = models.CharField(
        max_length=6,
        null=True, blank=True
    )
    user2 = models.CharField(
        max_length=6,
        null=True, blank=True
    )
    user1Choice = models.CharField(max_length=10,
                                   null=True, blank=True
                                   )
    user2Choice = models.CharField(max_length=10,
                                   null=True, blank=True
                                   )
    user1Score = models.IntegerField(default=0)
    user2Score = models.IntegerField(default=0)

    def __str__(self):
        return self.room_group_name()

    def room_group_name(self):
        return f"room_{self.id}"

    def is_full(self):
        return self.user1 and self.user2

    def joinUser(self):
        room = Room.objects.get(id=self.id)
        # check if the room is full or not
        if room.user1 and room.user2:
            # send the full signal
            pass
        else:
            id = get_id()
            if room.user1 is None:
                room.user1 = id
                # send the waiting signal
                async_to_sync(channel_layer.group_send)(
                    room.room_group_name(),
                    send_message({
                        'type': "waiting",
                        "userId": room.user1
                    })
                )
            else:
                room.user2 = id
                room.currentRound = 1
                # send the startGame signal
                async_to_sync(channel_layer.group_send)(
                    room.room_group_name(),
                    send_message({
                        'type': "startGame",
                        "userId": room.user2
                    })
                )

            room.save()

    def saveTurn(self, userId, turn):
        room = Room.objects.get(id=self.id)
        if room.user1 == userId:
            room.user1Choice = turn
        elif room.user2 == userId:
            room.user2Choice = turn
        room.save()

        winner = None
        if room.user1Choice is not None and room.user2Choice is not None:
            if room.user1Choice == room.user2Choice:
                # tie
                room.user1Score += 1
                room.user2Score += 1
            elif room.user1Choice == 'rock':
                if room.user2Choice == 'paper':
                    winner = room.user2
                    room.user2Score += 1
                elif room.user2Choice == 'scissor':
                    winner = room.user1
                    room.user1Score += 1
            elif room.user1Choice == 'paper':
                if room.user2Choice == 'rock':
                    winner = room.user1
                    room.user1Score += 1
                elif room.user2Choice == 'scissor':
                    winner = room.user2
                    room.user2Score += 1
            elif room.user1Choice == 'scissor':
                if room.user2Choice == 'rock':
                    winner = room.user2
                    room.user2Score += 1
                elif room.user2Choice == 'paper':
                    winner = room.user1
                    room.user1Score += 1

            # show the winner and
            # call the next level
            async_to_sync(channel_layer.group_send)(
                room.room_group_name(),
                send_message({
                    'type': "result",
                    "winner": winner,
                    "user1Choice": room.user1Choice,
                    "user2Choice": room.user2Choice,
                    "currentRound": room.currentRound,
                    "user1Score": room.user1Score,
                    "user2Score": room.user2Score
                })
            )
            room.currentRound += 1
            room.user1Choice = None
            room.user2Choice = None

        else:
            # send the opponentSelect Signal
            async_to_sync(channel_layer.group_send)(
                room.room_group_name(),
                send_message({
                    'type': "played",
                    "userId": userId
                })
            )
        room.save()

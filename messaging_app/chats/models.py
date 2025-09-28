from django.db import models
import uuid


# Create your models here.
class Users(models.Model):
    user_id = models.UUIDField(primary_key=True, 
                               default=uuid.uuid4,
                               editable=False,
                               unique=True, 
                               db_index=True)
    first_name = models.CharField(max_length=70, null=False)
    last_name = models.CharField(max_length=70, null=False)
    email = models.EmailField(max_length=70, unique=True, null=False)
    password_hash = models.CharField(max_length=120, null=False)
    phone_number = models.CharField(max_length=20)
    RoleChoice = models.TextChoices('Guest', 'Host', 'Admin')
    role = models.CharField(max_length=7,
                            choices=RoleChoice,
                            null=True,
                            blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    message_id = models.UUIDField(primary_key=True, 
                                  default=uuid.uuid4,
                                  db_index=True,
                                  unique=True)
    sender_id = models.ForeignKey(Users.user_id, on_delete=models.CASCADE)
    message_body = models.TextField(max_length=1000, null=False)
    sent_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    conversation_id = models.UUIDField(primary_key=True, 
                                       default=uuid.uuid4,
                                        db_index=True)
    participants_id = models.ForeignKey(Users.user_id, on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)

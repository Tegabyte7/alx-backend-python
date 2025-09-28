from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Users(AbstractUser):
    user_id = models.UUIDField(primary_key=True, 
                               default=uuid.uuid4,
                               editable=False,
                               unique=True, 
                               db_index=True)
    email = models.EmailField(max_length=70, unique=True, null=False)
    password_hash = models.CharField(max_length=120, null=False)
    phone_number = models.CharField(max_length=20)
    RoleChoice = models.TextChoices('Guest', 'Host', 'Admin')
    role = models.CharField(max_length=7,
                            choices=RoleChoice,
                            null=True,
                            blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.email} ({self.role})"
    

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



from django.db import models
from django.contrib.auth.models import User
from CustomUser.models import CustomUser
from PIL import Image
from django.utils import timezone
from datetime import timedelta
from .utils import generate_otp, send_otp_email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpeg', upload_to='profile_pics')
    otp = models.CharField(max_length=6, blank=True, null=True)
    otp_time = models.DateTimeField(blank=True, null=True)
    email_verified = models.BooleanField(default=False)

    def generate_and_send_otp(self):
        self.otp = generate_otp()
        self.otp_time = timezone.now()
        self.save()
        send_otp_email(self.user.email, self.otp)

    def otp_is_valid(self, otp_input):
        if self.otp == otp_input and self.otp_time + timedelta(minutes=10) > timezone.now():
            return True
        return False

    def __str__(self):
        return f'{self.user.username}Profile'

    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.image.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300,)
            img.thumbnail(output_size)
            img.save(self.image.path)


from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Profile

@receiver(user_signed_up)
def create_user_profile(sender, request, user, **kwargs):
    Profile.objects.get_or_create(user=user)

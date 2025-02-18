import random
from django.core.mail import send_mail

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user_email, otp):
    subject = "Your OTP for Verification"
    message = f"Your OTP for verification is: {otp}. It will expire in 10 minutes."
    send_mail(subject, message, 'darshpatel610@gmail.com', [user_email])
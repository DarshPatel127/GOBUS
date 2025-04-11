from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AddFundsForm
from exp.models import Wallet
from .models import Profile


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('account_login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    try:
        wallet = Wallet.objects.get(user=request.user)
    except Wallet.DoesNotExist:
        wallet = Wallet.objects.create(user=request.user, balance=0)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        add_funds_form = AddFundsForm(request.POST)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')
        elif 'add_funds' in request.POST and add_funds_form.is_valid():
            amount = add_funds_form.cleaned_data['amount']
            if amount <= 0 or amount > 10000000:
                messages.error(request, "Please enter a valid amount to add to your wallet.")
                return redirect('profile')
            wallet.balance += amount
            if wallet.balance < 0:
                messages.error(request, "You cannot have a negative balance in your wallet!")
                return redirect('profile')
            wallet.save()
            messages.success(request, f'₹{amount} has been added to your wallet!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
        add_funds_form = AddFundsForm()
    context = {
        'u_form': u_form,
        'p_form': p_form,
        'wallet': wallet,
        'add_funds_form': add_funds_form,
    }
    return render(request, 'users/profile.html', context)

@login_required
def send_otp(request):
    profile = request.user.profile
    profile.generate_and_send_otp()
    messages.info(request, "An OTP has been sent to your registered email address.")
    return redirect('otp_verification')  

@login_required
def verify_otp(request):
    if request.method == 'POST':
        otp_input = request.POST.get('otp')
        profile = request.user.profile
        if profile.otp_is_valid(otp_input):
            profile.otp = None
            profile.otp_time = None
            profile.email_verified = True
            profile.save()
            messages.success(request, "Your email has been verified successfully!")
            return redirect('profile')
        else:
            messages.error(request, "Invalid or expired OTP. Please try again.")
    return render(request, 'users/otp_verification.html')


from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, AddFundsForm
from exp.models import Wallet

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You are now able to login')
            return redirect('login')
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
            wallet.balance += amount
            wallet.save()
            messages.success(request, f'₹{amount} has been added to your wallet!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm( instance=request.user)
        p_form = ProfileUpdateForm( instance=request.user.profile)
        add_funds_form = AddFundsForm()
    context ={
        'u_form': u_form,
        'p_form': p_form,
        'wallet':wallet,
        'add_funds_form': add_funds_form,
    }
    return render(request, 'users/profile.html',context)
# Create your views here.

from django.shortcuts import render

def user_account(request):
    return render(request, 'users/user-acount.html')

def user_login(request):
    return render(request, 'users/user-login.html')

def user_register(request):
    return render(request, 'users/user-register.html')

def user_reset_password(request):
    return render(request, 'users/user-reset-password.html')

def user_wishlist(request):
    return render(request, 'users/user-wishlist.html')

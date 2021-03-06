from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth

# Create your views here.
def signup(request):
    if request.method == 'POST':
        for key in request.POST:
            if not request.POST[key]:
                return render(request, 'signup.html', {
                    'error': key + ' field is required'
                })

        if request.POST['password'] == request.POST['confirm_password']:
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {
                    'error': 'User name has already been taken'
                })
            except User.DoesNotExist:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password'])
                auth.login(request, user)
                return redirect('home')
        else:
            return render(request, 'signup.html', {
                'error': 'Passwords must match'
            })
    else:
        return render(request, 'signup.html')

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            next_url = request.POST.get('next_url')
            print(next_url)
            if next_url:
                return HttpResponseRedirect(next_url)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'username or password is incorrect'
            })
    else:
        return render(request, 'login.html', {
            'next_url': request.GET.get('next')
        })

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

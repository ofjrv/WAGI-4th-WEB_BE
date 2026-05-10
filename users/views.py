from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect


# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)


        if form.is_valid():
            form.save()
            return redirect('home')
        
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else :
            return render(request, 'users/login.html', {
                'error': '아이디 또는 비밀번호가 틀렸습니다.'
            })
        
    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('home')
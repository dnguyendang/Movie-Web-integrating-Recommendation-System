from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def Login_view(request):
    if request.method == 'POST':
        Login_form = AuthenticationForm(request,data=request.POST)
        if Login_form.is_valid():
            login(request, Login_form.get_user())
            return redirect('Home')
    else: 
        Login_form = AuthenticationForm()
    return render(request, 'Account/login.html', {'Login_form': Login_form})

def Register_view(request):
    if request.method == 'POST':
        Register_form = UserCreationForm(request.POST)
        if Register_form.is_valid():
            user = Register_form.save()
            login(request, user)
            return redirect('Home')
    else:
        Register_form = UserCreationForm()
    return render(request, 'Account/register.html', {'Register_form': Register_form})

def Logout_view(request):
    logout(request)
    return redirect('Home')






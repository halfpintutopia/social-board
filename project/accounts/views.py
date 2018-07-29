from django.contrib.auth import login
from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
# instead of using UserCreationForm to add the Email Field
from .forms import SignUpForm


def signup(request):
    """Logic of signup view."""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

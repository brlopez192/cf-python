from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


def login_view(request):
    error_message = None

    form = AuthenticationForm()
# When the user hits "login" button, then POST request is generated
    if request.method == 'POST':

# Read the data sent by the form via POST request
        form = AuthenticationForm(data=request.POST)

# Check if the form is valid
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

# Use Django autenticate function to validat the user
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('sales:records')
        else:
            error_message = "Oops! something went wrong."
    context = {
        'form': form,
        'error_message': error_message
    }
    return render(request, 'auth/login.html', context)


def logout_view(request):
    logout(request)
    return redirect('login')
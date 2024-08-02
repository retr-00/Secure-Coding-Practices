from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib import messages

def secure_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = make_password(password)
        user = MyUser(email=email, password=hashed_password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Registration successful!')
        return redirect('secure_login')
    return render(request, 'authapp/secure_register.html')

def secure_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, 'Login successful!')
            #return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid credentials')
    return render(request, 'authapp/secure_login.html')

# Insecure Registration View
def insecure_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')  # Capturing password as plain text
        # Directly saving the password as plain text
        user = MyUser(email=email, password=password)
        user.save()
        messages.add_message(request, messages.SUCCESS, 'Registration successful! But beware, this method is insecure.')
        return redirect('insecure_login')
    return render(request, 'authapp/insecure_register.html')


# Insecure Login View
def insecure_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = MyUser.objects.get(email=email)
            if user.password == password:  # Direct comparison of plaintext passwords
                # Not using Django's session framework correctly here
                request.session['user_id'] = user.id  # Not regenerating session ID
                messages.add_message(request, messages.SUCCESS, 'Login successful! But remember, this method is insecure.')
                #return redirect('home')
            else:
               messages.add_message(request, messages.ERROR, 'Invalid credentials')
        except MyUser.DoesNotExist:
            messages.error(request, 'User does not exist')
    return render(request, 'authapp/insecure_login.html')


def home(request):
    return render(request, 'authapp/home.html')
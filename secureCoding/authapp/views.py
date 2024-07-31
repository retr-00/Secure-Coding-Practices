from django.shortcuts import render, redirect
from .models import MyUser

def insecure_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')  # Insecure: saving password as plain text
        user = MyUser.objects.create(email=email, password=password)  # No hashing
        return redirect('insecure_login')
    return render(request, 'authapp/insecure_register.html')

def insecure_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = MyUser.objects.get(email=email)
            if user.password == password:  # Insecure: direct comparison
                return redirect('home')  # Redirect to a home page
            else:
                return render(request, 'authapp/insecure_login.html', {'error': 'Invalid login'})
        except MyUser.DoesNotExist:
            return render(request, 'authapp/insecure_login.html', {'error': 'User does not exist'})
    return render(request, 'authapp/insecure_login.html')

def secure_register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        MyUser.objects.create_user(email=email, password=password)  # Uses manager to hash password
        return redirect('secure_login')
    return render(request, 'authapp/secure_register.html')

def secure_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a home page
        else:
            return render(request, 'authapp/secure_login.html', {'error': 'Invalid credentials'})
    return render(request, 'authapp/secure_login.html')

def home(request):
    return render(request, 'authapp/home.html')
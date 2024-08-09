from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from .models import MyUser
from django.contrib import messages
from django_otp import devices_for_user
from django_otp.plugins.otp_totp.models import TOTPDevice
import qrcode
import qrcode.image.svg
from io import BytesIO
import base64



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
            # Redirect to the OTP verification page without displaying a login success message
            if any(device for device in devices_for_user(user)):
                return redirect('verify_2fa')
            else:
                messages.add_message(request, messages.WARNING, 'No OTP device found. Please set up 2FA.')
                return redirect('setup_2fa')
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

def setup_2fa(request):
    user = request.user

    # If the user already has a TOTP device, we will overwrite it with a new one
    device = None
    for existing_device in devices_for_user(user):
        if isinstance(existing_device, TOTPDevice):
            device = existing_device
            break

    # If no existing TOTP device was found, create a new one
    if not device:
        device = TOTPDevice.objects.create(user=user, name='default')

    device.confirmed = False  # Reset confirmation for the device

    # Generate QR code as PNG
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(device.config_url)
    qr.make(fit=True)

    # Create PNG image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer)  # Remove the format argument
    png_data = base64.b64encode(buffer.getvalue()).decode('utf-8')  # Encode the PNG to base64

    if request.method == 'POST':
        otp_token = request.POST.get('otp_token')
        if device.verify_token(otp_token):
            device.confirmed = True
            device.save()
            messages.add_message(request, messages.SUCCESS, '2FA setup successful and updated!')
            return redirect('secure_login')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid OTP. Please try again.')

    return render(request, 'authapp/setup_2fa.html', {'png_data': png_data})


def verify_2fa(request):
    if request.method == 'POST':
        otp_token = request.POST.get('otp_token')
        user = request.user
        for device in devices_for_user(user):
            if device.verify_token(otp_token):
                messages.add_message(request, messages.SUCCESS, 'Login successful!')
                return redirect('secure_login')
        messages.add_message(request, messages.ERROR, 'Invalid OTP token.')
    return render(request, 'authapp/verify_2fa.html')


    
def home(request):
    return render(request, 'authapp/home.html')

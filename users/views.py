from users.register import RegisterForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db import IntegrityError





def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.warning(request, 'Email already exists. Please choose a different email.')
                return redirect('register')

            try:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                confirmation_link = request.build_absolute_uri(f'/confirm-email/{uid}/{token}/')
                html_message = render_to_string('users/confirmation_email.html', {'confirmation_link': confirmation_link, 'user': user.email})
                send_mail(
                    'Confirm your email',
                    'Please confirm your email by clicking the link below.',
                    'agyekumoxgood@gmail.com',
                    [user.email],
                    html_message=html_message
                )
                return redirect('email_confirmation_sent')
            
            except IntegrityError as e:
                if 'auth_user.username' in str(e):
                    messages.error(request, 'Username already exists. Please try again.')
                    return redirect('register')
                else:
                    messages.error(request, 'An error occurred during registration. Please try again.')
                    return redirect('register')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})




def confirm_email(request, uidb64, token):
    user = get_user_model()
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = user.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('email_confirmed')
    else:
        return render(request, 'email_confirmation_invalid.html')

from django.http import HttpResponse, HttpResponseNotFound
from .models import Access_key
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.models import User
from django.contrib import messages

@login_required
def home(request):
    user = request.user
    access_keys = Access_key.objects.filter(user=user).order_by('-date_of_procurement')
    all_access_keys = Access_key.objects.all().order_by('-date_of_procurement')
    has_active_key = Access_key.objects.filter(user=user, status='active').exists()
    return render(request,'base/home.html',{'access_keys': access_keys,'all_access_keys': all_access_keys, 'has_active_key': has_active_key})



def request_new_key(request):
    user = request.user

    # Check if the user has an active key
    if Access_key.objects.filter(user=user, status='active').exists():
        return HttpResponseNotFound("Page does not exist")

    # Create a new key
    now = timezone.now()
    expiry = now + timezone.timedelta(hours=5)
    new_key = Access_key.objects.create(user=user, date_of_procurement=now, expiry_date=expiry)
    return redirect('home')


def search_key(request):
    key_details = None
    error_message = None
    status_code = ''
    if request.method == 'POST':
        
        school_email = request.POST.get('school_email')

        if not school_email:
            error_message = 'School email is required'
        else:
            try:
                # Search for the active key
                user = User.objects.filter(email=school_email).first()
                active_key = Access_key.objects.filter(user=user, status='active').first()
                
                if active_key:
                    key_details= {
                        'key_id': active_key.id,
                        'key_status': active_key.status,
                        'date_of_procurement': active_key.date_of_procurement,
                        'expiry_date': active_key.expiry_date,
                    }
                    status_code = 200
                else:
                    error_message = 'No active key found for this email'
                    status_code = 404
            except Exception as e:
                error_message = f'Error: {str(e)}'

    return render(request, 'base/endpoint.html', {'key_details': key_details, 'error_message': error_message, 'status_code':status_code})


def revoke_key(request, key_id):
    # Ensure the user is an admin
    if not (request.user.is_authenticated and request.user.is_superuser):
        return HttpResponseNotFound('Forbidden')
    key_id = key_id
    
    return render(request,'base/confirm_revoke.html',{'key_id':key_id})  

def confirm_revoke_key(request, key_id):
    # Ensure the user is an admin
    if not request.user.is_authenticated and not request.user.is_superuser:
        return HttpResponseNotFound('Page Not Found')  # Redirect to an appropriate view

    # Get the key object
    key = get_object_or_404(Access_key, id=key_id)
    
    # Change the status to 'revoked'
    key.status = 'revoked'
    key.save()

    # Add a success message
    messages.success(request, f"Key {key.id} has been successfully revoked.")

    
    return redirect('home')  
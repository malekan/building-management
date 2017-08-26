from .models import Profile
from django.shortcuts import get_object_or_404


def profiles_processor(request):
    user_fullname = get_object_or_404(Profile, user=request.user).full_name
    return {
        'user_fullname': user_fullname,
    }

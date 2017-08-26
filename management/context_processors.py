from .models import Profile


def profiles_processor(request):
    try:
        user_fullname = Profile.objects.get(user=request.user).full_name
    except Profile.DoesNotExist:
        return {}
    return {
        'user_fullname': user_fullname,
    }

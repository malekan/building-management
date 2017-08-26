from .models import Profile


def profiles_processor(request):
    try:
        if request.user.is_authenticated():
            user_fullname = Profile.objects.get(user=request.user).full_name
        else:
            return {}
    except Profile.DoesNotExist:
        return {}
    return {
        'user_fullname': user_fullname,
    }

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile
from .forms import ProfileForm


# Create your views here.
def home_view(request):
    """
    Home page view - accessible to all users
    """
    return render(request, 'profiles/home.html')


@login_required
def profile_view(request):
    """
    Loads the profile page - logged in users only
    """
    user = request.user
    edit_mode = request.GET.get('edit', False)

    try:
        profile = user.profile
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=user)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
            edit_mode = True
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'user': user,
        'profile': profile,
        'profile_form': profile_form,
        'edit_mode': edit_mode,
    }

    return render(request, 'profiles/profile.html', context)
